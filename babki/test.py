from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import flash
from datetime import timedelta

import uuid
from markupsafe import escape

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#app.permanent_session_lifetime = timedelta(minutes=1)

print(" * Start")

@app.route("/n<name>")
def showName(name):
    return f"Hello, {escape(name)}!"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)



@app.route('/')
def index():
    ok = False
    tex = ''
    if 'username' in session:
        tex += f'Logged in as {session["username"]}<br>'
    if 'email' in session:
        tex += f'Email: {session["email"]}<br>'
    if 'role' in session:
        tex += f'Role: {session["role"]}<br>'
    if tex != '':
        return tex
    
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #session.permanent = True
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        session['role'] = request.form['role']  # Например, роль пользователя
        print('new session')
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=email name=email>  <!-- Добавляем поле для адреса электронной почты -->
            <p><input type=text name=role>  <!-- Добавляем поле для роли пользователя -->
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

'''
@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

def valid_login(username, password):
    # Здесь можно добавить проверку имени пользователя и пароля в базе данных или другой логикой
    # В данном примере, пусть будет успешной, если имя пользователя и пароль не пустые
    return bool(username and password)

def log_the_user_in(username):
    return f'Logged in as: {username}'

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    searchword = request.args.get('key', 'def')
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    
    return render_template('login.html', error=error, searchword=searchword)

'''


@app.route('/get_dynamic_text', methods=['GET'])
def get_dynamic_text():
    # Ваш код здесь для генерации динамического текста
    dynamic_text = "Next card ЖДИТЕ"
    return dynamic_text





@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/register/<username>', methods=['GET', 'POST'])
def register_user(username):
    user_id = str(uuid.uuid4())  # Генерация UUID
    # Далее вы можете сохранить user_id в базу данных или использовать его как угодно
    return f'User "{escape(username)}" registered with ID: {escape(user_id)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'