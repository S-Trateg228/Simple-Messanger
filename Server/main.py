import json

import requests
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

import threading
import cryptography
from random import randint as rnd

app = Flask(__name__)

app.config['SECRET_KEY'] = 'EYE_OF_DEVIL'

app.config['MYSQL_USER'] = 'RIPPER'
app.config['MYSQL_DB'] = 'users'
app.config['MYSQL_PASSWORD'] = ''

mysql = MySQL(app)


@app.route('/to_server')
def ping():
    return 'WE WILL CONTROL THE FUCK PING'


@app.route('/get_info', methods=['GET', 'POST'])
def authorization_func():  # Авторизация
    if request.method == 'POST':
        try:
            login = request.json['login']
            password = request.json['password']
            cursor = mysql.connection.cursor()

            cursor.execute('''INSERT INTO UsersBase (login, password) VALUES ('{0}', '{1}')'''.format(login, password))

            mysql.connection.commit()

            cursor.close()

            return 'OK'
        except BaseException:
            return 'ERROR OF AUTHORIZATION'
    else:
        return None


@app.route('/send_message', methods=['GET', 'POST'])
def get_user_message():  # Получение на сервер сообщения отправленного пользователем
    if request.method == 'POST':
        user = request.json['user']
        sender = request.json['sender']
        message = request.json['message']

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO MessageBase (login, sender, message, chat_id) VALUES ({0}, "{1}", "{2}", {3})'''.format(user, sender, message, rnd(0, 10)))

        mysql.connection.commit()

        cursor.close()

        return 'ok'


@app.route('/send_image', methods=['GET', 'POST'])
def get_user_image():  # Получение картинки и ее загрузка в мессенджере NOT WORKING
    if request.method == 'POST':
        user = request.json['user']
        image = request.json['image']

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO image_base (id, user, image) VALUES ({0}{1}{2})'''.format(1, user, image))

        mysql.connection.commit()

        cursor.close()


@app.route('/send_document', methods=['GET', 'POST'])
def get_user_document():  # Получение документа NOT WORKING
    if request.method == 'POST':
        user = request.json['user']
        document = request.json['document']

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO document_base (id, user, document) VALUES ({0}{1}{2})'''.format(1, user, document))

        mysql.connection.commit()

        cursor.close()


@app.route('/check_new_messages', methods=['GET', 'POST'])
def check_new_messages():  # проверка наличия на сервере новых сообщений
    if request.method == 'GET':
        user = request.json['user']
        id_last_message = request.json['id_last_message']
        chat_id = request.json['chat_id']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT message FROM MessageBase WHERE id > {0} AND login = "{1}"'.format(id_last_message, user))
        main_str = str()

        for i in cursor.fetchall():
            main_str += i[0] + '%%%'
        return jsonify(main_str)


if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)).start()
    #app.run(host='localhost', port=8080, debug=True, use_reloader=False)


'''
login:RIPPER
password:123
'''

'''
request.post('http://127.0.0.1/get_info', json={'login': login, 'password': password})
request.post('http://127.0.0.1/send_message', json={'login': login, 'sender': sender, 'chat_id': chat_id})

requests.get('http://10.110.127.80:8080/check_new_messages', json={'user': 'RIPPER', 'id_last_message': 0, 'chat_id': 1}).content

'''
