from app import ClientApp
from network import Session

IP = 'localhost'
PORT = 3578

if __name__ == "__main__":
    session = Session(IP, PORT)
    ClientApp().run()