import datetime
import config as config
from flask import Flask, request, render_template, flash, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user
from wtforms_alchemy import ModelForm


app = Flask(__name__, template_folder="templates")
app.config.from_object(config)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model):
    def __init__(self, username, password, email, name, surname):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.surname = surname

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, index=True)
    username = db.Column(db.String(64), unique = True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    surname = db.Column(db.String(10), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(10000), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    article_url = db.Column(db.String(500),unique=True, nullable=False)
    date_created = db.Column(db.Date, default=datetime.datetime.now())
    is_visible = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False,
                        index=True)
    user = db.relationship(User, foreign_keys=[user_id, ])

    def __str__(self):
        return '<Post {0}>'.format(self.content)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.Date, default=datetime.datetime.now())
    is_visible = db.Column(db.Boolean, default=True)
    article_id = db.Column(db.Integer,
                           db.ForeignKey('article.id'),
                           nullable=False,
                           index=True)
    article = db.relationship(Article, foreign_keys=[article_id, ])

    def __str__(self):
        return '<Comment {0}>'.format(self.content)


class ArticleForm(ModelForm):
    class Meta:
        model = Article


class CommentForm(ModelForm):
    class Meta:
        model=Comment


@login_manager.user_loader
def load_user(id):
    """
    Возвращается текущий зарегистрированный пользователь
    :param id: id текущего зарегистрированного
    :return: пользователь
    """
    return User.query.get(int(id))


@app.before_request
def before_request():
    """
    Инициализация пользователя до запроса
    :return: None
    """
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    """
    Обработчик события: перейти на главную страницу
    :return: шаблон главной страницы
    """
    posts = Article.query.all()
    return render_template('index.html', posts = posts, user = g.user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Регистрация нового пользователя
    :return: переход на страницу для авторизации
    """
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    name = request.form['name']
    surname = request.form['surname']
    user = User(username, password, email, name, surname)
    db.session.add(user)
    db.session.commit()
    flash('Пользователь успешно зарегистрирован')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Аутентификация зарегистрированного пользователя
    :return: главная страница с доступными ссылками на статьи
    """
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Неправильный логин или пароль', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Авторизация успешно пройдена')
    return redirect(url_for('index'))


@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    """
    Форма для добавления нового поста
    :return: возвращает на главную страницу, если пост добавлен успешно
    """
    if request.method == 'GET':
        return render_template('personal_text.html', user=username)
    if request.method == 'POST':
        form = ArticleForm(request.form)
        if form.validate():
            post = Article(user_id=g.user.id, **form.data)
            db.session.add(post)
            db.session.commit()
            flash('Новый пост успешно создан!')
            return redirect(url_for('index'))
        else:
            return (str(form.errors))


@app.route('/post/<article_url>', methods=['GET'])
def post(article_url):
    """
    Полный текст статьи с комментариями
    :return: страницу с текстом статьи
    """
    if request.method == 'GET':
        art = Article.query.filter_by(article_url = article_url).first()
        comm = Comment.query.filter_by(article = art)
        return render_template('page_article.html', post = art, comments = comm)
    if request.method == 'POST':
        form = CommentForm(request.form)
        if form.validate():
            current_post = Article.query.filter_by(article_url = article_url).first()
            post = Comment(article = current_post, article_id = current_post.id, **form.data)
            db.session.add(post)
            db.session.commit()
            flash('Новый комментарий успешно создан!')
            return redirect(url_for('article/article_url'))
        else:
            return (str(form.errors))


@app.route('/logout', methods=['GET'])
def logout():
    """
    Выйти из системы
    :return: переход на главную страницу
    """
    if request.method == 'GET':
        logout_user()
        return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run()
