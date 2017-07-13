import os, random
from flask import Flask, request, jsonify, session
from flask_wtf import FlaskForm
from wtforms import validators, DecimalField, StringField

os.environ["FLASK_RANDOM_SEED"] = "100"
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='This key',
    WTF_CSRF_ENABLED=False,
)
scope = int(os.environ["FLASK_RANDOM_SEED"])
random.seed(scope)
digit = None


def new_current_number():
    """
    Получение нового рандомного числа
    :return: None
    """
    global digit
    digit = random.randint(1, scope)


@app.route('/', methods=['GET'])
def hidden_number():
    """
    Функция обработки запроса к главной странице
    :return: строка
    """
    new_current_number()
    return "Новое число загадано"


class GuessForm(FlaskForm):
    username = StringField(label='Имя', validators=[
        validators.DataRequired()
    ])
    digit_guess = DecimalField(label='Отгаданное число', validators=[
        validators.DataRequired()
    ])


@app.route('/guess', methods=['POST'])
def user_guess():
    form = GuessForm(request.form)
    if form.validate():
        if 'username' not in session:
            session['username'] = request.form['username']
            session['current_number'] = digit
            session['count_digit'] = 0
            session["count_guess"] = 0
        print(session)
        if form.digit_guess.data > digit:
            session["count_guess"] += 1
            print(session)
            return "Ваше число больше загаданного"
        elif form.digit_guess.data < digit:
            session["count_guess"] += 1
            print(session)
            return "Ваше число меньше загаданного"
        else:
            session['count_digit'] += 1
            new_current_number()
            session['current_number'] = digit
            print(session)
            return "Вы угадали число. Новое число загадано"
    else:
        error = form.errors
        return jsonify(valid='1', errors=dict(error))

if __name__ == '__main__':
    app.run()
