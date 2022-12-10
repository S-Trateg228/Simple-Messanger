from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

import threading
import cryptography


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
        message = request.json['message']

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO MessageBase (id, user, message) VALUES ({0}{1}{2})'''.format(1, user, message))

        mysql.connection.commit()

        cursor.close()


@app.route('/send_image', methods=['GET', 'POST'])
def get_user_image():  # Получение картинки и ее загрузка в мессенджере
    if request.method == 'POST':
        user = request.json['user']
        image = request.json['image']

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO image_base (id, user, image) VALUES ({0}{1}{2})'''.format(1, user, image))

        mysql.connection.commit()

        cursor.close()


@app.route('/send_document', methods=['GET', 'POST'])
def get_user_document():  # Получение документа
    if request.method == 'POST':
        user = request.json['user']
        document = request.json['document']

        cursor = mysql.connection.cursor()

        cursor.execute('''INSERT INTO document_base (id, user, document) VALUES ({0}{1}{2})'''.format(1, user, document))

        mysql.connection.commit()

        cursor.close()

@app.route('/check_new_messages', methods=['GET', 'POST'])
def check_new_messages():
    user = request.json['user']
    id_last_message = request.json['id_last_message']

    cursor = mysql.connection.cursor()

    cursor.execute('SELECT * FROM MessageBase WHERE id > {0} AND user = {1}'.format(id_last_message, user))
    print(cursor.description)


if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='localhost', port=8080, debug=True, use_reloader=False)).start()
    #app.run(host='localhost', port=8080, debug=True, use_reloader=False)


'''
login:RIPPER
password:123
'''

'''
request.post('http://127.0.0.1/get_info', json='login:{0}&&password:{1}'.format(login, password))
request.post('http://127.0.0.1/get_info', json='login:{0}&&password:{1}'.format(login, password))
'''
