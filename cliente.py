import socket
from _thread import *

class Network():

    def reciever(self):
        while True:
            data = self.client.recv(4096)
            print("aqui")
            self.last_response = data.decode()
            if(self.last_response.startswith("play")):
                if self.last_response.split("/")[1] == "ready":
                    self.ready = True
                else:
                    self.ready = False

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 1330
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

    def close(self):
        self.client.close()