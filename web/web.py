from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# 设置你的用户名和密码
USER_NAME = '123'
PASSWORD = '123'

# HTML模板，加入了CSS样式
LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
    <style>
        body, html {
            height: 100%;
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
        }
        .login-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 20px;
            background: #f2f2f2;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        input[type=text], input[type=password] {
            width: 100%;
            padding: 15px;
            margin: 5px 0 22px 0;
            display: inline-block;
            border: none;
            background: #f1f1f1;
        }
        input[type=text]:focus, input[type=password]:focus {
            background-color: #ddd;
            outline: none;
        }
        input[type=submit] {
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            cursor: pointer;
            width: 100%;
            opacity: 0.9;
        }
        input[type=submit]:hover {
            opacity:1;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <form method="post">
            <label for="username">Username:</label><br>
            <input type="text" name="username" required><br>
            <label for="password">Password:</label><br>
            <input type="password" name="password" required><br>
            <input type="submit" value="Login">
        </form>
    </div>
</body>
</html>
'''

SUCCESS_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login Success</title>
</head>
<body>
    <h2>Login Successful!</h2>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USER_NAME and password == PASSWORD:
            return render_template_string(SUCCESS_PAGE)
        else:
            return 'Login Failed. Please try again.'
    return render_template_string(LOGIN_PAGE)

if __name__ == '__main__':
    app.run(debug=True)
