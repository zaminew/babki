
import uuid
from markupsafe import escape
from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_login import current_user, login_required
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data', 'site.db')
#app.config['SECRET_KEY'] = 'your_secret_key'
# FIXME СКРЫТЬ ВСЕ КЛЮЧИ vvvvvvvvvvvvvvv
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# TODO СКРЫТЬ ВСЕ КЛЮЧИ ^^^^^^^^^^^^^^

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# test
stubUserRating=777

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(50), nullable=False)



    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.before_request
def before_request():
    pages = [
        {'url': url_for('index'), 'name': 'Главная'},
        {'url': url_for('login'), 'name': 'Войти'},
        {'url': url_for('register'), 'name': 'Регистрация'},
        {'url': url_for('profile'), 'name': 'Профиль'},
        {'url': url_for('posts'), 'name': 'Посты'},
        {'url': url_for('add_post'), 'name': 'Добавить пост'},
        {'url': url_for('logout'), 'name': 'Выйти'}
    ]
    g.pages = pages
    g.stubUserRating = stubUserRating



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            # Обработка неверного логина или пароля
            return render_template('login.html', error='Неверный логин или пароль')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('register.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
    #return f'Hello, {current_user.username}!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))








@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        text = request.form['text']
        author = current_user.username
        post = Post(text=text, author=author)
        db.session.add(post)
        db.session.commit()

    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        text = request.form['text']
        author = current_user.username
        post = Post(text=text, author=author)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))

    return render_template('add_post.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

