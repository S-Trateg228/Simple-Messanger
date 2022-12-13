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
        answer: requests.Response = requests.post(f"http://{self.ip}:{self.port}/send_message", json={'user': 'RIPPER', 'id_last_message': -5, 'chat_id': 0})
        #print(answer.status_code, answer.content)
        print(answer.text)
        #try:
            
        #except requests.RequestException:
            #print('No connection')
        '''try:
            self.RSA()
        except requests.RequestException:
            print('No signal! Try again')'''

    def RSA(self):
        power = random.randint(50, 100)
        sent_message = (BASE ** power) % MOD
        answer = requests.post(self.ip + ':' + self.port, data=json.dumps(sent_message))
        self.key = (sent_message ** answer) % MOD
#print(json.dumps({"login":"RIPPER", "password": "123"}))
if __name__ == "__main__":
    #print("send")
    #print(f"http://192.168.195.164:8080/get_info/")
    #a = requests.post(url=f"http://192.168.1.68:8080/get_info", json={"login":"RIPPER", "password": "123"})
    #print(a.text)
    Session('192.168.1.68', '8080').connect()

'''
login:...
password:hash(...)
'''