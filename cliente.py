import socket
from _thread import *
import sys
import os

def limpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimeTabuleiro(tabuleiro):

    # Limpa a tela
    limpaTela()

    # Imprime coordenadas horizontais
    dim = len(tabuleiro)
    sys.stdout.write("     ")
    for i in range(dim):
        sys.stdout.write("{0:2d} ".format(i))

    sys.stdout.write("\n")

    # Imprime separador horizontal
    sys.stdout.write("-----")
    for i in range(dim):
        sys.stdout.write("---")

    sys.stdout.write("\n")

    for i in range(dim):

        # Imprime coordenadas verticais
        sys.stdout.write("{0:2d} | ".format(i))

        # Imprime conteudo da linha 'i'
        for j in range(dim):

            # Peca ja foi removida?
            if tabuleiro[i][j] == '-':

                # Sim.
                sys.stdout.write(" - ")

            # Peca esta levantada?
            elif tabuleiro[i][j] >= 0:

                # Sim, imprime valor.
                sys.stdout.write("{0:2d} ".format(tabuleiro[i][j]))
            else:

                # Nao, imprime '?'
                sys.stdout.write(" ? ")

        sys.stdout.write("\n")

def imprimePlacar(placar):

    nJogadores = len(placar)

    print("Placar:")
    print("---------------------")
    for i in range(nJogadores):
        print("Jogador {0}: {1:2d}".format(i + 1, placar[i]))

def imprimeStatus(tabuleiro, placar, vez):

        imprimeTabuleiro(tabuleiro)
        sys.stdout.write('\n')

        imprimePlacar(placar)
        sys.stdout.write('\n')
        sys.stdout.write('\n')

        print("Vez do Jogador {0}.\n".format(vez + 1))


class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 1332
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
                elif type_of_m == "*":
                    print(m[2:])
                    self.close()
                    sys.exit()
                else:
                    print(m)


    def close(self):
        self.client.close()

c = Client()
c.receiveMessages()



