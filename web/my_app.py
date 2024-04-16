from flask import Flask, render_template, redirect, flash, request, session, send_file, make_response
from flask_mail import Mail, Message
import pymssql
import hashlib
import random, string, base64, os
from captcha.image import ImageCaptcha
    
app = Flask(__name__)

app.secret_key = 'QiChen_specialKey' #cookies
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'qipublic11@gmail.com'
app.config['MAIL_PASSWORD'] = 'druykvpazezleseu'
app.config['MAIL_DEFAULT_SENDER'] = ('QiChen', 'qipublic11@gmail.com')

mail = Mail(app)


file_abs_path = os.path.abspath(__file__)
file_path = os.path.dirname(file_abs_path)
#connect to sql database
db = pymssql.connect(
    server = 'qiscerver.database.windows.net',
    port = '1433',
    user = 'QiChen',
    password = 'Cq020613',
    database = 'QiChenDatabase',
    charset = 'utf8',
    as_dict = True
)

cursor = db.cursor()


#command to database
def createUser(username,password,email,verifyCode,illness):
    sql = "insert into users(Username,Password,Email,VerifyCode,Illness) values('"+username+"','"+password+"','"+email+"','"+verifyCode+"','"+illness+"')"
    #sql = 'update students set name=%s where id=%s'
    #sql = 'delete from students where id<%s'
    cursor.execute(sql)
    db.commit()

def deleteUser(key, value):
    sql = 'delete from users where ' + str(key) + '=%s'
    cursor.execute(sql,(value))
    db.commit()

def detectUser(key, value):
    sql = 'select * from users where ' + str(key) + '=%s'
    cursor.execute(sql,(value))
    detected_user = cursor.fetchall()
    return detected_user

def loginUser(username, password):
    sql = 'select * from users where username=%s and password=%s'
    cursor.execute(sql,(username,password))
    exist_user = cursor.fetchall()
    return exist_user

def user_logged_in():
    if 'username' in session:
        return 1
    else:
        return 0

def encode_password(password):
    ePw=hashlib.md5()
    ePw.update('try to encode this'.encode('utf-8'))
    ePw.update(password.encode('utf-8'))
    return str(ePw.hexdigest())

def generate_Code(length):
    characters = string.ascii_letters + string.digits
    Code = ''.join(random.choice(characters) for i in range(length))
    return Code

def generate_captcha():  
    captcha = generate_Code(4)
    #creating captcha img
    img = ImageCaptcha(width=200)
    img.generate(captcha)
    img.write(captcha, 'static/images/captcha.png')
    return captcha

def send_code(email):
    session['code'] = generate_Code(6)
    message = Message(subject="Verify Code", recipients=[email])
    message.body = "Your verify code is " + session['code']
    mail.send(message)


#website
@app.route('/')
def index():
    if 'username' in session:
        flash('Welcome, user:' + session['username'])
    else:
        flash("Welcome, you haven't login")
    return render_template('home.html', user_logged_in=user_logged_in())    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        captcha = request.form['captcha']
        password = encode_password(password)
        if session['captcha'].lower() == captcha.lower():
            if len(loginUser(username, password)) > 0:
                session['username'] = username
                flash('successfully login!')
                return redirect('/')
            else:
                flash('Username or password incorrect!')
        else:
            flash('captcha incorrect!')
    return render_template('login.html', user_logged_in=user_logged_in())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #get form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        illness = request.form['ill']
        verifyCode = request.form['verify_code']
        #encode password
        password = encode_password(password)
        #check
        if len(detectUser('username', username)) > 0:
            flash('Username existing')
        elif verifyCode == "":
            send_code(email)
        elif session['code'] == verifyCode:
            createUser(username,password,email,verifyCode, illness)
            flash('Successfully registered!')
            return redirect('/login')
        else:
            flash('Wrong verify code')
    return render_template('register.html', user_logged_in=user_logged_in())

@app.route('/logout')
def logout():
    if not user_logged_in():
        return render_template('return.html', info="You need to login first!")
    session.pop('username', None)
    flash('Logout successfully')
    return redirect('/')

@app.route('/data')
def dataPreform():
    if not user_logged_in():
        return render_template('return.html', info="You need to login first!")
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return render_template('dataPreform.html', users=users, user_logged_in=user_logged_in())

@app.get('/data/<user_id>')
def user_id(user_id):
    if not user_logged_in():
        return render_template('return.html', info="You need to login first!")
    sql = 'SELECT * FROM users where id = %s'
    cursor.execute(sql, (user_id))
    users = cursor.fetchall()
    return render_template('dataPreform.html', users=users, user_logged_in=user_logged_in())

@app.post("/search")
def search():
    user_name = request.form['user_name']
    if len(detectUser('username', user_name)) == 0:
        flash("Username is not existed")
        return redirect('/data')
    else:
        sql = 'select * from users where username=%s'
        cursor.execute(sql, (user_name))
        users = cursor.fetchall()
        return redirect('/data/' + str(users[0]['id']))
    
@app.get("/captcha")
def captcha():
    captcha = generate_captcha()
    session['captcha'] = captcha
    return send_file(file_path + '/static/images/captcha.png', mimetype='image/png')

cursor.close

if __name__ == '__main__':
    app.run()