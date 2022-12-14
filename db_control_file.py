from flask import request
from flask_mysqldb import MySQL


def check_user(cursor: MySQL().connection, special_flag=False) -> bool:
    login = request.json['login']
    hash = request.json['hash']

    if special_flag:
        password = request.json['password']

        sql = '''
            SELECT * FROM UsersBase WHERE login = '{0}' AND hash = '{1}' AND password = '{2}'
        '''
    else:
        sql = '''
            SELECT * FROM UsersBase WHERE login = '{0}' AND hash = '{1}'
        '''.format(login, hash)

    cursor.execute(sql)

    if len(cursor.fetchall()) != 0:
        return True

    return False
