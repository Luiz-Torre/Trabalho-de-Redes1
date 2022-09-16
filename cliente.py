import socket
from _thread import *

class Client():

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 1331
        self.addr = (self.server,self.port)
        self.ready = False
        self.id = self.connect()
        self.last_response = ""
        start_new_thread(self.reciever, ())

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, msg):
        # print("enviou: " + msg.decode())
        try:
            self.client.send(msg)
        except socket.error as e:
            print(e)

    def reciever(self):
        while True:
            data = self.client.recv(1024)
            print("aqui")
            self.last_response = data.decode()
            print(f"Received {data!r}")
            if(self.last_response.startswith("play")):
                if self.last_response.split("/")[1] == "ready":
                    self.ready = True
                else:
                    self.ready = False

    def close(self):
        self.client.close()


HOST = "localhost"  # The server's hostname or IP address
PORT = 1331  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")