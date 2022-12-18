import requests
import hashlib
import os.path as path
import uuid
from cryptography.fernet import Fernet
import base64

class Session():
    "Общается с сервером."
    
    def __init__(self, ip: str, port: str):
        """Инициализация сессии.

        :param ip: ip-адрес сервера
        :type ip: str
        
        :param port: порт сервера
        :type port: str
        """
        self.ip = ip
        self.port = port
        self.login = ''
        self.password = ''
        main_hash = hashlib.sha256()
        mac_address = hex(uuid.getnode())[2:]
        main_hash.update(mac_address.encode())
        self.hashed_mac_address = main_hash.hexdigest()
        
    
    def ping(self) -> bool:
        """Проверяет доступность сервера.

        :returns: True - сервер отвечает
        :rtype: bool
        """
        try:
            requests.get(f"http://{self.ip}:{self.port}/to_server")
            return True
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return False
    
    def connect(self, login: str, password: str, is_registration: bool) -> bool:
        """Авторизация или регистрация на сервере.

        :param login: логин
        :type login: str

        :param password: пароль
        :type password: str
        
        :param is_registration: True - для регистрации, False - для авторизации
        :type is_registration: bool

        :returns: ответ от сервера
        :rtype: bool
        """
        try:
            answer: requests.Response = requests.post(f"http://{self.ip}:{self.port}/get_info", 
                                                      json={'login': login, 
                                                            'password': password, 
                                                            'is_register': 'reg' if is_registration else 'auth', 
                                                            'mac_address': self.hashed_mac_address})
            print(answer.text)
            return answer.text == 'OK' or answer.text == 'yes'
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            print("No connection!")
            return False
        '''try:
            self.RSA()
        except requests.RequestException:
            print('No signal! Try again')'''

    def get_new_messages(self, chat_name: str, last_message_id: int) -> tuple[bool, list[list[int, str, str, str]]]:
        """Получение сообщений определённого чата, начиная с некоторого номера.

        :param chat_name: чат
        :type chat_name: str

        :param last_message_id: номер последнего известного сообщения
        :type last_message_id: int

        :returns: Первое значение: True в случае успеха получения данных с сервера.
        Второе значение: список состоящий из: индекс сообщения, текст, отправитель, время отправки.
        :rtype: tuple[bool, list[list[int, str, str, str]]]:
        """
        try:
            answer: requests.Response = requests.get(f"http://{self.ip}:{self.port}/check_new_messages", 
                                                     json={"login": self.login, 
                                                           "user2": chat_name, 
                                                           "id_last_message": last_message_id, 
                                                           'mac_address': self.hashed_mac_address})
            messages = answer.json()
            print(messages)
            success = True
            if not path.isfile(f"Client/keys/{chat_name}.txt"):
                success = self.update_keys()
            if success:
                if not path.isfile(f"Client/keys/{chat_name}.txt"):
                    self.send_key(chat_name)
                with open(f"Client/keys/{chat_name}.txt", 'rb') as f_key:
                    key = f_key.read()
                for list_index, (idx, ciphered_text, sender, time) in enumerate(messages.copy()):
                    if ciphered_text.startswith("FILE"):
                        file_code = ciphered_text[4:]
                        self.write_file("document1", file_code)
                        messages[list_index][1] = f"You got document from {chat_name}! Check folder 'files'"
                    else:
                        print(key, ciphered_text)
                        text = str(Fernet(key).decrypt(bytes(ciphered_text, 'utf-8')), 'utf-8')
                        messages[list_index][1] = text
                return (True, messages)
            else:
                return (False, [])
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return (False, [])

    def send_message(self, chat_name: str, text: str, time: str) -> bool:
        """Отправка сообщения на сервер.

        :param chat_name: чат
        :type chat_name: str

        :param text: текст сообщения
        :type text: str
        
        :param time: время отправки
        :type time: str

        :returns: True в случае успеха отправки сообщения на сервер
        :rtype: bool:
        """
        try:
            key = ''
            self.update_keys()
            if not path.isfile(f"Client/keys/{chat_name}.txt"):
                success = self.send_key(chat_name)
                if not success:
                    return success
                
            with open(f"Client/keys/{chat_name}.txt", 'rb') as f_key:
                key = f_key.read()
            print(key)
            
            cipher = Fernet(key)
            ciphered_text = str(cipher.encrypt(bytes(text, encoding='utf-8')), encoding='utf-8')
            answer: requests.Response = requests.post(f"http://{self.ip}:{self.port}/send_message", 
                                                      json={"login": self.login, 
                                                            "password": self.password, 
                                                            "receiver": chat_name, 
                                                            "message": ciphered_text, 
                                                            "time": time,
                                                            'mac_address': self.hashed_mac_address})
            print(answer.text, "status of sending")
            return answer.text == 'ok'
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return False

    def find_chats(self, chat_name: str) -> tuple[bool, list[str]]:
        """Поиск чата по части имени на сервере.

        :param chat_name: чат
        :type chat_name: str

        :returns: Первое значение: True в случае успеха получения данных с сервера.
        Второе значение: список найденных чатов. 
        :rtype: tuple[bool, list[str]]:
        """
        try:
            answer: requests.Response = requests.get(f"http://{self.ip}:{self.port}/find_users", 
                                                     json={"login": self.login, "find_user": chat_name, 'mac_address': self.hashed_mac_address})
            return (True, [element_list[0] for element_list in answer.json()])
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return (False, [])

    def get_all_chats(self) -> tuple[bool, list[str]]:
        """Получение всех чатов, с кем ведётся переписка.

        :returns: Первое значение: True в случае успеха получения данных с сервера.
        Второе значение: список своих чатов. 
        :rtype: tuple[bool, list[str]]:
        """
        try:
            answer: requests.Response = requests.get(f"http://{self.ip}:{self.port}/get_all_my_users", 
                                                     json={"login": self.login, 'mac_address': self.hashed_mac_address})
            
            return (True, answer.json())
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return (False, [])

    def send_key(self, chat_name: str) -> bool:
        try:
            key = Fernet.generate_key()
            answer: requests.Response = requests.post(f"http://{self.ip}:{self.port}/keys_exchange", 
                                                     json={"login": self.login, "receiver": chat_name, 'mac_address': self.hashed_mac_address, 'key': key.decode('utf-8')})
            if answer.content == b'OK':
                with open(f"Client/keys/{chat_name}.txt", 'wb') as f_key:
                    f_key.write(key)
                return True
            else:
                return False
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return False 

    def update_keys(self):
        try:
            answer: requests.Response = requests.get(f"http://{self.ip}:{self.port}/keys_exchange", 
                                                     json={"login": self.login, 'mac_address': self.hashed_mac_address})
            for chat_name, key in answer.json():
                key = bytes(key, encoding='utf-8')
                with open(f"Client/keys/{chat_name}.txt", 'wb') as f_key:
                    f_key.write(key)
            return True
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return False

    def send_file(self, chat_name: str, filename: str, time: str) -> bool:
        if not path.isfile(f"Client/files/{filename}"):
            return False

        file = open(f"Client/files/{filename}", 'rb')
        final = "FILE" + base64.b64encode(file.read()).decode()
        file.close()
        try:
            print('post started')
            answer: requests.Response = requests.post(f'http://{self.ip}:{self.port}/send_message',
                                                      json={'login': self.login, 
                                                            'receiver': chat_name, 
                                                            'mac_address': self.hashed_mac_address, 
                                                            'message': final,
                                                            'time': time})
            print('post ended with code ', answer.content)
            return answer.content == b'ok'
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return False
        
    def write_file(self, filename: str, code: str):
        file = open(f"Client/files/{filename}", 'wb')
        file.write(base64.b64decode(code.encode()))
        file.close()

#if __name__ == "__main__":
#    Session('192.168.1.1', '8080').connect("R", "123")
f = open("Client/server_address.txt")
IP, PORT = f.readline().split(':')
f.close()

s = Session(IP, PORT)
'''
s.login = 'debug'
s.password = 'debug'
s.send_message("debuging", "HELLO", "11.11.1111 11:11")
'''
#s.login = 'debuging'
#s.password = 'debuging'
#print(s.get_key())

