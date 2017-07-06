from flask import Flask, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField
import datetime, os


app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret key',
    WTF_CSRF_ENABLED=False,
)


@app.route('/locales')
def json_array():
    """
    Выдает данные при переходе по ссылке /locales
    :return:массив в формате json
    """
    language = ['ru', 'en', 'it']
    return jsonify(languages=language)


@app.route('/meta')
def obtain_info_from_request():
    """
    Вывод параметров запроса к серверу
    :return: json-объект
    """
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    headers = dict(request.headers)
    query = dict(request.args)
    return jsonify(current_date=str(date),
                   current_time=str(time),
                   received_headers=headers,
                   received_query_args=query)


@app.route('/serve/<path:filename>')
def get_content_file(filename):
    """
    Получение содержимого файла из папки files
    :param filename: имя файла
    :return: содержимое файла
    """
    try:
        path_file = os.path.join('./files', filename)
        with open(path_file) as f:
            return f.read()
    except IOError:
        return "file not found", 404


@app.route('/form/user', methods=['POST'])
def processing_user_data():
    """
    Авторизация пользователя
    :return: результат проверки правильности введенных данных
    """
    form = RegistrationForm(request.form)
    if form.validate():
        return jsonify(valid='0',
                       errors='[]')
    else:
        error = form.errors
        return jsonify(valid='1',
                       errors=dict(error))


class RegistrationForm(FlaskForm):
    email = StringField(label='E-mail', validators=[
        validators.Email(),
        validators.DataRequired()
    ])
    password = PasswordField(label='password', validators=[
        validators.Length(min=6),
        validators.DataRequired()
    ])
    confirmation_password = PasswordField('Повторите пароль', validators=[
        validators.EqualTo('password', message='Пароли должны совпадать'),
        validators.DataRequired()
    ])


if __name__ == '__main__':
    app.run()
