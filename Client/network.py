import requests
import json
import random

BASE = 6
MOD = 23

class Session():

    def __init__(self, ip: str, port: str):
        self.ip = ip
        self.port = port
        self.login = ''
        self.password = ''

    def connect(self, login, password):
        try:
            answer: requests.Response = requests.post(f"http://{self.ip}:{self.port}/get_info", json={'login': login, 'password': password, 'is_register': 'auth'})
            print(answer.text)
            return answer.text == 'OK' or answer.text == 'yes'
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            print("No connection!")
        '''try:
            self.RSA()
        except requests.RequestException:
            print('No signal! Try again')'''

    def get_new_messages(self, chat_name, last_message_id):
        print('try to get')
        answer: requests.Response = requests.get(f"http://{self.ip}:{self.port}/check_new_messages", json={"user": self.login, "user2": chat_name, "id_last_message": last_message_id})
        print('Success')
        print(answer.json())
        return answer.json()

    def send_message(self, chat_name, text, time):
        answer: requests.Response = requests.post(f"http://{self.ip}:{self.port}/send_message", json={"login": self.login, "password": self.password, "sender": chat_name, "message": text, "time": time})
        print(answer.text, "status of sending")

    def find_chats(self, chat_name):
        answer: requests.Response = requests.get(f"http://{self.ip}:{self.port}/find_users", json={"find_user": chat_name})
        return [element_list[0] for element_list in answer.json()]
        
    
    def get_all_chats(self):
        answer: requests.Response = requests.get(f"http://{self.ip}:{self.port}/get_all_my_users", json={"login": self.login})
        print(answer.content)
        return answer.json()

    def RSA(self):
        power = random.randint(50, 100)
        sent_message = (BASE ** power) % MOD
        answer = requests.post(self.ip + ':' + self.port, data=json.dumps(sent_message))
        self.key = (sent_message ** answer) % MOD
if __name__ == "__main__":
    Session('192.168.1.1', '8080').connect("R", "123")
