import unittest
import requests


class SendMessageTest(unittest.TestCase):
    def test_one(self):
        res = requests.post('http://127.0.0.1:8080/send_message',
             json={'login': 'RIPPER', 'sender': 'hacker111', 'mac_address': 'secret', 'message': 'hello',
                   'time': '11.11.1111 11:11'}).content
        self.assertEqual(res, 'ok')

    def test_two(self):
        pass

    def test_three(self):
        pass

    def test_four(self):
        pass


class Registration_AuthenticationTests(unittest.TestCase):
    def test_one(self):
        pass

    def test_two(self):
        pass

    def test_three(self):
        pass


class GetAllUsers(unittest.TestCase):
    def test_one(self):
        pass

    def test_two(self):
        pass


class FindUser(unittest.TestCase):
    def test_one(self):
        pass

    def test_two(self):
        pass


class CheckNewMessages(unittest.TestCase):
    def test_one(self):
        pass

    def test_two(self):
        pass


class KeysExchange(unittest.TestCase):
    def test_one(self):
        pass

    def test_two(self):
        pass



