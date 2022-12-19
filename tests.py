import unittest
import requests
import base64


class SendMessageTest(unittest.TestCase):  # 100% TESTS PASSED
    def test_ok_response(self):  # Провекра успешной отправки сообщения
        res = requests.post('http://127.0.0.1:8080/send_message',
             json={'login': 'RIPPER', 'receiver': 'EFA', 'mac_address': 'b865286216da99bf3313cf37a69a6836e44c43004229729f5f376151dc0936aa', 'message': 'hello',
                   'time': '11.11.1111 11:11'}).content.decode()
        self.assertEqual(res, 'ok')

    def test_two(self):  # Запрос с ошибкой
        res = requests.post('http://127.0.0.1:8080/send_message',
             json={'login': 'RIPPER', 'sender': 'NOT_USER', 'mac_address': 'b865286216da99bf3313cf37a69a6836e44c43004229729f5f376151dc0936aa', 'message': 'hello',
                   'time': '11.11.1111 11:11'}).content.decode()
        self.assertEqual(res, 'ERROR. NOT ENOUGH NECESSARY INFORMATION.')

    def test_file_send(self):  # Успешная отправка файла
        file = open('files/icon.png', 'rb')
        final = 'FILE' + base64.b64encode(file.read()).decode()
        file.close()

        res = requests.post('http://127.0.0.1:8080/send_message',
                            json={'login': 'RIPPER', 'receiver': 'EFA', 'mac_address': 'b865286216da99bf3313cf37a69a6836e44c43004229729f5f376151dc0936aa', 'message': final,
                                  'time': '11.11.1111 11:11'}).content.decode()
        print(res)
        self.assertEqual(res, 'ok')

    def test_four(self):  # Отправка слишком большого файла
        file = open('files/26m.pdf', 'rb')
        final = base64.b64encode(file.read()).decode()
        file.close()

        res = requests.post('http://127.0.0.1:8080/send_message',
                            json={'login': 'RIPPER', 'receiver': 'EFA', 'mac_address': 'b865286216da99bf3313cf37a69a6836e44c43004229729f5f376151dc0936aa', 'message': final,
                                  'time': '11.11.1111 11:11'}).content.decode()

        self.assertEqual(res, 'FILE IS TOO LARGE')


class Registration_AuthenticationTests(unittest.TestCase):  # 100% TESTS PASSED
    def test_reg_success(self):  # 12:44:83:8c:a6:fa
        res = requests.post('http://127.0.0.1:8080/get_info',
                            json={'is_register': 'reg', 'login': 'RIPPER_test', 'password': 'hack123',
                                  'mac_address': '8615602dd3c54be6daac4c4384a860ad068f61fc5431c92932c9b4c0b03369eb'}).content.decode()

        self.assertEqual(res, 'OK')

    def test_reg_error(self):
        res = requests.post('http://127.0.0.1:8080/get_info',
                            json={'is_register': 'reg', 'login': 'RIPPER_fall', 'password': 'hack123'}).content.decode()

        self.assertEqual(res, 'ERROR. NOT ENOUGH NECESSARY INFORMATION.')

    def test_auth_success(self):
        res = requests.post('http://127.0.0.1:8080/get_info',
                            json={'is_register': 'auth', 'login': 'RIPPER', 'password': 'divide_et_empera', 'mac_address': 'b865286216da99bf3313cf37a69a6836e44c43004229729f5f376151dc0936aa'}).content.decode()

        self.assertEqual(res, 'yes')

    def test_auth_error(self):
        res = requests.post('http://127.0.0.1:8080/get_info',
                            json={'is_register': 'auth', 'login': 'RIPPER', 'password': 'hack12321', 'mac_address': 'secret'}).content.decode()

        self.assertEqual(res, 'no')


class GetAllUsers(unittest.TestCase):  # 100 TESTS PASSED
    def test_success(self):
        res = requests.get('http://127.0.0.1:8080/get_all_my_users',
                            json={'login': 'RIPPER', 'mac_address': 'b865286216da99bf3313cf37a69a6836e44c43004229729f5f376151dc0936aa'}).json()

        self.assertEqual(type(res), list)

    def test_error(self):
        res = requests.get('http://127.0.0.1:8080/get_all_my_users',
                            json={'login': 'fgkjk;fjg', 'mac_address': 'ee87231bc75c3302fabf88e2ed817af7302969184d4f941ee20c4b44704dc282'}).content.decode()

        self.assertEqual(res, 'ACCESS DENIED')
        


class FindUser(unittest.TestCase):  # 100% TESTS PASSED
    def test_success(self):
        res = requests.get('http://127.0.0.1:8080/find_users',
                            json={'login': 'RIPPER', 'mac_address': 'b865286216da99bf3313cf37a69a6836e44c43004229729f5f376151dc0936aa', 'find_user': 'EF'}).json()

        self.assertEqual(type(res), list)

    def test_error(self):
        res = requests.get('http://127.0.0.1:8080/find_users',
                            json={'log': 'as', 'mac_address': ''}).content.decode()

        self.assertEqual(res, 'ERROR. NOT ENOUGH NECESSARY INFORMATION.')


class CheckNewMessages(unittest.TestCase):  # 100% TESTS PASSED
    def test_success(self):
        res = requests.get('http://127.0.0.1:8080/check_new_messages',
                            json={'login': 'DEBUGGER', 'user2': 'debug', 'mac_address': '2b:3d:44:34:c5:31', 'id_last_message': 12}).json()

        self.assertEqual(type(res), list)

    def test_error(self):
        res = requests.get('http://127.0.0.1:8080/check_new_messages',
                            json={'login1': 'abc', 'user2': 'abc', 'mac_address': ''}).content.decode()

        self.assertEqual(res, 'ERROR. NOT ENOUGH NECESSARY INFORMATION.')


class KeysExchange(unittest.TestCase):  # 100% TESTS PASSED
    def test_success(self):
        res = requests.post('http://127.0.0.1:8080/keys_exchange',
                            json={'login': 'RIPPER', 'receiver': 'EFA', 'key': 'KEY', 'mac_address': 'b865286216da99bf3313cf37a69a6836e44c43004229729f5f376151dc0936aa'}).content.decode()

        self.assertEqual(res, 'OK')

    def test_error(self):
        res = requests.post('http://127.0.0.1:8080/keys_exchange',
                            json={'login': 'RIPPER', 'receiver': '1', 'key': 'key', 'mac_address': 'b86586216da99bf3313cf37a69a6836e44c43004229729f5f376151dc0936aa'}).content.decode()

        self.assertEqual(res, 'ACCESS DENIED')
