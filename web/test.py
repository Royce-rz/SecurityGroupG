#import pymssql
from flask import Flask, render_template, redirect, flash, request, session, send_file, make_response
from flask_mail import Mail, Message
import pymssql
import hashlib
import random, string, base64, os
from captcha.image import ImageCaptcha  
import os
'''
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
'''
#connect to sql database
from flask import Flask
from flask_mail import Mail, Message

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

def send_email():
    with app.app_context():
        # 创建邮件消息
        msg = Message(
            subject="Verify Code",
            recipients=["chenqiinsane@163.com"],
            body="This is a test email from Flask-Mail."
        )
        # 发送邮件
        mail.send(msg)
        print("Email sent successfully!")

if __name__ == "__main__":
    send_email()

#command to database
def createUser():
    username = input("username:")
    password = input("password:")
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
    if detected_user == 1:
        print("Username existing")
        return 1
    else:
        return 0



def login():
    username = input("username:")
    password = input("password:")
    sql = 'select * from users where username=%s and password=%s'
    cursor.execute(sql,(username,password))
    exist_user = cursor.fetchall()
    if len(exist_user) == 1:
        return 0
    else:
        return 1

#command to cursor

#sql = 'create table if not exists users(id int auto_increment, username varchar(255) not null,password varchar(255) not null, primary key (id))'
'''
#createUser()
sql = 'select * from users'
#sql = 'delete from users where id>0'
#sql = 'drop table users'
cursor.execute(sql)
all_d = cursor.fetchall()
print("data:",all_d)
cursor.close
'''




sql = '''IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[users]') AND type in (N'U'))
BEGIN
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(255) NOT NULL,
    password NVARCHAR(255) NOT NULL
)
END
'''