import socket
from _thread import *
import sys
import os


class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 1331
        self.addr = (self.server, self.port)
        self.ready = False
        self.id = self.connect()
        self.last_response = ""

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

    def receiveMessages(self):
        print("Waiting for server message...")
        while True:
            data = self.client.recv(1024)
            self.last_response = data.decode()

            #Processar mensagens
            messages = self.last_response.split("#")[:-1]
            for m in messages:
                type_of_m = m[0]

                #Se for uma ação
                if type_of_m == ">":
                    #Mandar coordenadas
                    coordenadas = input(m[2:])
                    self.send(coordenadas.encode())
                #Se for um erro
                elif type_of_m == "+":
                    print(m[2:])
                #Se não for para pular linha
                elif type_of_m == "%":
                    print(m[2:], end =" ")
                #Se acabou o jogo
                elif type_of_m == "*":
                    print(m[2:])
                    self.close()
                    return
                else:
                    print(m)


    def close(self):
        self.client.close()

c = Client()
c.receiveMessages()



