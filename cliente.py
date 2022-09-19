import socket
from _thread import *

class Client():

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 1331
        self.addr = (self.server, self.port)
        self.ready = False
        self.id = self.connect()
        self.last_response = ""
        start_new_thread(self.receiver, ())

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(1024).decode().split(":")[1]
        except:
            print("Failed to connect.")
            pass

    def send(self, msg):
        # print("enviou: " + msg.decode())
        try:
            self.client.send(msg)
        except socket.error as e:
            print(e)

    def receiver(self):
        while True:
            data = self.client.recv(1024)
            self.last_response = data.decode()
            print(f"Received {data!r}")
            #Processar mensagens
            

            #Executar


    def close(self):
        self.client.close()

c = Client()



