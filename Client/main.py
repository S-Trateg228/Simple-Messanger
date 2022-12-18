from app import ClientApp

f = open("server_address.txt")
IP, PORT = f.readline().split(':')
f.close()

if __name__ == "__main__":
    ClientApp(IP, PORT).run()