import json
import sys
import threading

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

from db_control_file import check_user, check_time_format

app = Flask(__name__)

app.config['SECRET_KEY'] = 'EYE_OF_DEVIL'

app.config['MYSQL_USER'] = 'RIPPER'
app.config['MYSQL_DB'] = 'users'
app.config['MYSQL_PASSWORD'] = ''
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

mysql = MySQL(app)


@app.route('/to_server')
def ping():  # Проверка роботоспособности сервера
    return 'SERVER WORKS'


@app.route('/keys_exchange', methods=['GET', 'POST'])
def exchange_keys():
    '''
    Функция для обмена ключами. отправляет в виде json логины отправителя, получателя, ключ

    :return: возвращает OK если обмен ключами прошел успешно
    '''
    try:
        if not check_user(mysql, special_flag=False):
            return 'ACCESS DENIED'

        cursor = mysql.connection.cursor()

        login = request.json['login']

        if request.method == 'POST':
            receiver = request.json['receiver']
            key = request.json['key']

            cursor.execute(
                '''INSERT INTO UsersKey 
                (login1, login2, cipher_key_12)
                 VALUES ('{0}', '{1}', '{2}')'''.format(login, receiver, key))
            mysql.connection.commit()

            cursor.close()

            return 'OK'
        elif request.method == 'GET':
            sql = '''
                SELECT login1, cipher_key_12 FROM UsersKey WHERE login2 = '{0}'
            '''

            cursor.execute(sql.format(login))
            base = cursor.fetchall()

            return jsonify(base)
    except TypeError:
        return 'ERROR. DATABASE HAS NOT APPROPRIATE DATA OR REQUIRED INFORMATION WAS NOT SENT TO THE SERVER.'
    except KeyError:
        return 'ERROR. NOT ENOUGH NECESSARY INFORMATION.'


@app.route('/get_info', methods=['POST'])
def authorization_func():
    '''
    Реализует авторизацию при auth-запросе и регистрацию при reg-запросе
    При помощи json может принимать логин, пароль, хешированный MAC-адресс

    :return: отчет о выполнении запроса
    '''
    if request.method == 'POST':
        try:
            is_register = request.json['is_register']
            if is_register == 'reg':
                login = request.json['login']
                password = request.json['password']
                mac_address = request.json['mac_address']
                cursor = mysql.connection.cursor()

                cursor.execute(
                    '''INSERT INTO UsersBase (login, password, mac_address) VALUES ('{0}', '{1}', '{2}')'''.format(
                        login, password, mac_address))

                mysql.connection.commit()

                cursor.close()
            elif is_register == 'auth':
                user = request.json['login']
                password = request.json['password']

                cursor = mysql.connection.cursor()
                sql = '''
                                SELECT login, password FROM UsersBase WHERE login = '{0}' AND password = '{1}'
                            '''.format(user, password)
                cursor.execute(sql)
                if len(cursor.fetchall()) != 0:
                    return 'yes'
                else:
                    return 'no'

            return 'OK'
        except TypeError:
            return 'ERROR. DATABASE HAS NOT APPROPRIATE DATA OR REQUIRED INFORMATION WAS NOT SENT TO THE SERVER.'
        except KeyError:
            return 'ERROR. NOT ENOUGH NECESSARY INFORMATION.'
        except BaseException:
            return 'ERROR OF IDENTIFICATION'


@app.route('/send_message', methods=['POST'])
def get_user_message():
    '''
    Получение на сервер сообщения отправленного пользователем
    При помощи json принимает логины отправителя и получателя, а также сообщение

    :return: при успешной отправке на сервер сообщения, возвращает 'ok'
    '''
    if request.method == 'POST':
        try:
            if not check_user(mysql, special_flag=False):
                return 'ACCESS DENIED'

            login = request.json['login']
            receiver = request.json['receiver']
            message = request.json['message']

            if sys.getsizeof(message) >= 200000:
                return 'FILE IS TOO LARGE'

            time = request.json['time']

            if not check_time_format(time):
                print(time, 'AAAAAAAAAAAAAAAA')
                return 'ERROR OF TIME FORMAT'

            cursor = mysql.connection.cursor()

            cursor.execute(
                '''INSERT INTO MessageBase (login, sender, message, time)
                 VALUES ('{1}', "{0}", "{2}", '{3}')'''.format(
                    login, receiver, message, time))

            mysql.connection.commit()

            cursor.close()

            return 'ok'
        except TypeError:
            return 'ERROR. DATABASE HAS NOT APPROPRIATE DATA OR REQUIRED INFORMATION WAS NOT SENT TO THE SERVER.'
        except KeyError:
            return 'ERROR. NOT ENOUGH NECESSARY INFORMATION.'
        except BaseException:
            return 'ERROR OF SENDING MESSAGE'


@app.route('/check_new_messages', methods=['GET'])
def check_new_messages():
    '''
    Проверка наличия на сервере новых сообщений
    При помощи json принимает логины отправителя и получателя сообщения, а также id
    последнего сообщения

    :return: возвращает json, содержащий новые сообщения заданного пользователя
    '''
    if request.method == 'GET':
        try:
            if not check_user(mysql, special_flag=False):
                return 'ACCESS DENIED'

            user = request.json['login']
            user2 = request.json['user2']
            id_last_message = request.json['id_last_message']

            sql = '''SELECT id, message, sender, time FROM MessageBase
             WHERE id > {0} AND (login = "{1}" AND sender = "{2}" OR login = "{2}" AND sender = "{1}")
            '''

            cursor = mysql.connection.cursor()
            cursor.execute(sql.format(id_last_message, user, user2))
            base = cursor.fetchall()
            return json.dumps(base)
        except TypeError:
            return 'ERROR. DATABASE HAS NOT APPROPRIATE DATA OR REQUIRED INFORMATION WAS NOT SENT TO THE SERVER.'
        except KeyError:
            return 'ERROR. NOT ENOUGH NECESSARY INFORMATION.'
        except BaseException:
            return 'ERROR OF SENDING MESSAGE'


@app.route('/find_users', methods=['GET'])
def find_user():
    '''
    Поиск пользователей по логину
    При помощи json отправляетя приблизительный логин искомого пользователя

    :return: возвращает список людей с указанным логином
    '''
    if request.method == 'GET':
        try:
            if not check_user(mysql, special_flag=False):
                return 'ACCESS DENIED'

            find_user = request.json['find_user']

            cursor = mysql.connection.cursor()
            sql = '''
                SELECT login FROM UsersBase WHERE login LIKE '{0}%'
            '''.format(find_user)
            cursor.execute(sql)

            return jsonify(cursor.fetchall())
        except TypeError:
            return 'ERROR. DATABASE HAS NOT APPROPRIATE DATA OR REQUIRED INFORMATION WAS NOT SENT TO THE SERVER.'
        except KeyError:
            return 'ERROR. NOT ENOUGH NECESSARY INFORMATION.'
        except BaseException:
            return 'ERROR OF FINDING USER'



@app.route('/get_all_my_users', methods=['GET'])
def get_all_my_users():
    '''
    Поиск всех людей, с кем общается пользователь
    Данный поиск осуществляется по логину пользовтеля, который отправляется при помощи json

    :return: Возвращает список людей, с кем общается пользователь или ответ, что пользователей
    нет, если пользователь не имеет ни одного чата
    '''

    if request.method == 'GET':
        try:
            if not check_user(mysql, special_flag=False):
                return 'ACCESS DENIED'

            login = request.json['login']

            cursor = mysql.connection.cursor()
            sql = '''
                SELECT login, sender FROM MessageBase WHERE sender = '{0}' OR login = '{0}'
            '''.format(login)
            cursor.execute(sql)
            base_unique = set()
            base = cursor.fetchall()

            if len(base) == 0:
                return jsonify(list())

            for el1, el2 in base:
                base_unique.add(el1)
                base_unique.add(el2)
            base_unique.remove(login)

            return jsonify(list(base_unique))

        except TypeError:
            return 'ERROR. DATABASE HAS NOT APPROPRIATE DATA OR REQUIRED INFORMATION WAS NOT SENT TO THE SERVER.'
        except KeyError:
            return 'ERROR. NOT ENOUGH NECESSARY INFORMATION.'
        except BaseException:
            return 'ERROR OF GETTING USERS'


if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)).start()

'''
login:RIPPER
password:123
'''

'''
request.post('http://127.0.0.1/get_info', json={'login': login, 'password': password})
request.post('http://127.0.0.1/send_message', json={'login': login, 'sender': sender, 'chat_id': chat_id})

requests.get('http://10.110.127.80:8080/check_new_messages', json={'user': 'RIPPER', 'id_last_message': 0, 'chat_id': 1}).content

'''

'''
import hashlib
main_hash = hashlib.sha256()
mac_address = 'your_mac_address'
main_hash.update(mac_address.encode())
final_hash = main_hash().hexdigest()
'''

'''
TESTS
**********

post('http://127.0.0.1:8080/get_info', json={'is_register': 'reg', 'login': 'RIPPER', 'password': 'hack123', 'mac_address': 'secret'})

post('http://127.0.0.1:8080/send_message', json={'login': 'RIPPER', 'sender': 'hacker111', 'mac_address': 'secret', 'message': 'hello', 'time': '11.11.1111 11:11'})


post('http://127.0.0.1:8080/send_message', json={'login': 'RIPPER', 'sender': 'hacker111', 'hash': 'secret', 'message': 'hello', 'time': '11.11.1111 11:11'})


post('http://127.0.0.1:8080/send_message', json={'login': 'RIPPER', 'sender': 'hacker111', 'hash': 'secret', 'message': 'hello', 'time': '11.11.1111 11:11'})


post('http://127.0.0.1:8080/send_message', json={'login': 'RIPPER', 'sender': 'hacker111', 'hash': 'secret', 'message': 'hello', 'time': '11.11.1111 11:11'})


post('http://127.0.0.1:8080/send_message', json={'login': 'RIPPER', 'sender': 'hacker111', 'hash': 'secret', 'message': 'hello', 'time': '11.11.1111 11:111'})

post('http://127.0.0.1:8080/send_message', json={'login': 'RIPPER', 'sender': 'hacker111', 'hash': 'secret', 'message': 'hello', 'time': '11.11.1111 11:111'})

post('http://127.0.0.1:8080/send_message', json={'login': 'RIPPER', 'sender': 'hacker111', 'hash': 'secre1t', 'message': 'hello', 'time': '11.11.1111 11:11'})

get('http://127.0.0.1:8080/get_all_my_users', json={'login': 'wolf', 'hash': 'mac'}).content
'''
