from flask import request
from flask_mysqldb import MySQL
from time import strptime

def check_user(mysql, special_flag=False) -> bool:
    '''
    Проверка запроса. Необходима для того, чтобы к серверу могли обращаться только
    зарегестрированные в мессенджере пользовтели

    :param mysql: объект базы данных
    :param special_flag: указывает на дополнительную проверку пароля
    :return: возвращает True если пользователь зарегестрирован в мессенджере
    '''
    cursor = mysql.connection.cursor()
    login = request.json['login']
    hash = request.json['mac_address']

    if special_flag:
        password = request.json['password']

        sql = '''
            SELECT * FROM UsersBase WHERE login = '{0}' AND mac_address = '{1}' AND password = '{2}'
        '''
    else:
        sql = '''
            SELECT * FROM UsersBase WHERE login = '{0}' AND mac_address = '{1}'
        '''.format(login, hash)

    cursor.execute(sql)

    if len(cursor.fetchall()) != 0:
        cursor.close()
        return True

    cursor.close()
    return False


TIME_FORMAT = "%d.%m.%Y %H:%M"

def check_time_format(time: str) -> bool:
    """Проверяет совпадает ли формат времени со следующим DD.MM.YYYY hh:mm.

        :param time: время для проверки
        :type time: str

        :returns: True - формат совпадает
        :rtype: bool
    """
    try:
        strptime(time, TIME_FORMAT)
        return True
    except ValueError:
        return False
