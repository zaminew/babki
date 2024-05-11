import sys
sys.path.append('/root/myDocker/babki/game_core')
import uuid
from markupsafe import escape
from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_login import current_user, login_required
import os

from game_core.game_controller import GameController
from game_core.game_setting import *


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

game_controller = GameController()

pls = ['id1', 'id2']


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniq_id = db.Column(db.String(36), unique=True, nullable=False)
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
    return User.query.get(user_id)



@app.before_request
def before_request():
    pages = [
        {'url': url_for('index'), 'name': 'Главная'},
        {'url': url_for('game_info'), 'name': 'Информация об игре'},
        {'url': url_for('create_game'), 'name': 'Создать игру'},
        {'url': url_for('game_play'), 'name': 'Играть'},
        {'url': url_for('get_dynamic_text'), 'name': 'get'},
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
    return render_template('index.html', games = game_controller.get_games_info())


@app.route('/game_play/')
@app.route('/game_play/<name>')
def game_play(name=None):
    return render_template('game_play.html', name=name)

@app.route('/get_dynamic_text', methods=['GET'])
def get_dynamic_text():
    dynamic_text = "Next card ЖДИТЕ"
    return dynamic_text


@app.route('/game_info', methods=['GET'])
def game_info():
    game_id = request.args.get('game_id')
    game_data = game_controller.games.get(game_id)
    
    if game_data:
        players = game_data.players
        return render_template('game_info.html', game_id=game_id, game_settings=game_data.settings.to_json(), game_players=players, game_maker=game_data.game_maker_id)
    else:
        return "Game not found", 404

@app.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    if request.method == 'POST':
        num_players = int(request.form['num_players'])
        speed = Speed(request.form['speed'])
        difficulty = Difficulty(request.form['difficulty'])
        game_type = GameType(request.form['game_type'])
        game_mode = GameMode(request.form['game_mode'])
        hide_stats = True if 'hide_stats' in request.form else False
        
        game_id = game_controller.create_game(GameSetting(num_players=num_players, speed=speed,
                                                           difficulty=difficulty, game_type=game_type,
                                                           game_mode=game_mode, hide_stats=hide_stats))
        game_controller.games[game_id].add_player(current_user.uniq_id, current_user.username)
        game_data = game_controller.games.get(game_id)
        if game_data:
            return redirect(url_for('game_info', game_id=game_id))
        else:
            return "Game not found", 404

    return render_template('create_game.html', Speed=Speed, Difficulty=Difficulty, GameType=GameType, GameMode=GameMode)

@app.route('/add_player_to_game/<game_id>, ', methods=['POST'])
@login_required
def add_player_to_game(game_id):
    game_data = game_controller.games.get(game_id)
    if not game_data:
        return "Game not found", 404
    
    game_controller.games[game_id].add_player(current_user.uniq_id, current_user.username)
    # Добавление объекта в игру, например:
    # object_id = request.form['object_id']
    # game_data.add_object(object_id)
    
    return redirect(url_for('game_info', game_id=game_id))

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
        uniq_id = str(uuid.uuid4())
        user = User(uniq_id=uniq_id, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        #session['uniq_id'] = uniq_id  # Сохраняем uniq_id в сессии
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

