import requests
import json
import random

BASE = 6
MOD = 23

class Session():

    def __init__(self, ip: str, port: str):
        self.ip = ip
        self.port = port

    def connect(self):
        try:
            answer: requests.Response = requests.post(json.dumps({"login":"RIPPER", "password": "123"}))
            print(answer.status_code, answer.content)
        except requests.RequestException:
            print('No connection')
        '''try:
            self.RSA()
        except requests.RequestException:
            print('No signal! Try again')'''

    def RSA(self):
        power = random.randint(50, 100)
        sent_message = (BASE ** power) % MOD
        answer = requests.post(self.ip + ':' + self.port, data=json.dumps(sent_message))
        self.key = (sent_message ** answer) % MOD

if __name__ == "__main__":
    Session('localhost', '8080').connect()

'''
login:...
password:hash(...)
'''