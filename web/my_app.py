from flask import Flask, render_template, redirect, flash, request, session
import pymssql

app = Flask(__name__)
app.secret_key = 'your_secret_key' #cookies

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
def createUser(username, password):
    try:
        sql = "insert into users(username,password) values('"+username+"','"+password+"')"
        #sql = 'update students set name=%s where id=%s'
        #sql = 'delete from students where id<%s'
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

def detectUser(username):
    sql = 'select * from users where username=%s'
    cursor.execute(sql,(username))
    detected_user = cursor.fetchall()
    if len(detected_user) > 0:
        return 1
    else:
        return 0


def loginUser(username, password):
    sql = 'select * from users where username=%s and password=%s'
    cursor.execute(sql,(username,password))
    exist_user = cursor.fetchall()
    if len(exist_user) > 0:
        return 1
    else:
        return 0

def user_logged_in():
    if 'username' in session:
        return 1
    else:
        return 0



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
        if loginUser(username, password):
            session['username'] = username
            flash('successfully login!')
            return redirect('/')
        else:
            flash('Falure')
    return render_template('login.html', user_logged_in=user_logged_in())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
 
        if detectUser(username):
            flash('Username existing')
        else:
            createUser(username, password)
            flash('Successfully registered!')
            return redirect('/login')
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
    if not detectUser(user_name):
        flash("Username is not existed")
        return redirect('/data')
    else:
        sql = 'select * from users where username=%s'
        cursor.execute(sql, (user_name))
        users = cursor.fetchall()
        return redirect('/data/' + str(users[0]['id']))

cursor.close

if __name__ == '__main__':
    app.run()