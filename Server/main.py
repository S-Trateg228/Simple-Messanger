from flask import Flask, request, jsonify
import flask_sqlalchemy
from flask_mysqldb import MySQL

import threading
import cryptography


app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)


@app.route('/to_server')
def ping():
    return 'WE WILL CONTROL THE FUCK WORLD'


@app.route('/get_info', methods=['GET', 'POST'])
def authorization_func():  # Авторизация
    if request.method == 'POST':
        data = jsonify(request.json)
        login = str(data.data).split('&&')[0].split(':')[1][:]
        password = str(data.data).split('&&')[1].split(':')[1][:-4]

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO user_pass (id, login, password) VALUES ({0}{1}{2})'''.format(1, login, password))

        mysql.connection.commit()

        cursor.close()

        return data
    else:
        return None


@app.route('/send_message', methods=['GET', 'POST'])
def get_user_message():  # Получение на сервер сообщения отправленного пользователем
    if request.method == 'POST':
        data = jsonify(request.json)
        user = str(data.data).split('&&')[0].split(':')[1][:]
        message = str(data.data).split('&&')[1].split(':')[1][:-4]

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO message_base (id, user, message) VALUES ({0}{1}{2})'''.format(1, user, message))

        mysql.connection.commit()

        cursor.close()


@app.route('/send_image', methods=['GET', 'POST'])
def get_user_image():  # Получение картинки и ее загрузка в мессенджере
    if request.method == 'POST':
        data = jsonify(request.json)
        user = str(data.data).split('&&')[0].split(':')[1][:]
        image = str(data.data).split('&&')[1].split(':')[1][:-4]

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO image_base (id, user, image) VALUES ({0}{1}{2})'''.format(1, user, image))

        mysql.connection.commit()

        cursor.close()


@app.route('/send_document', methods=['GET', 'POST'])
def get_user_document():  # Получение документа
    if request.method == 'POST':
        data = jsonify(request.json)
        user = str(data.data).split('&&')[0].split(':')[1][:]
        document = str(data.data).split('&&')[1].split(':')[1][:-4]

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO document_base (id, user, document) VALUES ({0}{1}{2})'''.format(1, user, document))

        mysql.connection.commit()

        cursor.close()


if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='localhost', port=8080, debug=True, use_reloader=False)).start()

'''
login:RIPPER
password:123
'''
