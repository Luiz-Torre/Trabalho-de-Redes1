import socket
from socket import socket as Socket
from _thread import *
import sys


class Server:

    HOST = "localhost"  # IP local
    PORT = 1331         # porta escolhida para conexão
    socket = None       # socket do servidor, sem valor atribuído
    clients = []        # lista de clientes conectados
    playersConnected = False
    messageBuffer = []

    def start(n_players: int):
        ''' Função para inicializar o servidor. '''
        Server.socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
    
        try:
            Server.socket.bind((Server.HOST, Server.PORT))
        except socket.error as e:
            print(e)
            sys.exit()  
        Server.socket.listen()
        start_new_thread(Server.start_t,(n_players,))
        
    def resetServerInfo():
        ''' Função para resetar o servidor ao final do jogo. '''
        Server.clients = []
        Server.playersConnected = False
        Server.messageBuffer = []

    def start_t(n_players: int): 
        ''' Thread criada para esperar N conexões com o servidor. '''
        while True:
            print("Aguardando jogadores...")

            conn, addr = Server.socket.accept()
            n_clients = len(Server.clients) 

            Server.clients.append(conn)
            Server.messageBuffer.append([])
            print(f"{addr} está conectado.")

            #Manda para o player seu ID no servidor   
            conn.send(str.encode(f"id:{n_clients+1}"))

            start_new_thread(Server.client_t, (conn, n_clients+1))

            if n_clients + 1 >= n_players:
                print("Jogadores conectados.")
                Server.playersConnected = True
                break
                

    def client_t(conn: Socket, id: int):
        ''' Thread criada para receber mensagens dos clientes. '''
        while True:
            try:
                data = conn.recv(4096) #Conexao recebe

                if not data:
                    #Cliente se desconectou do servidor
                    print("Player " + str(id) + " disconnected")
                    Server.clients[id - 1] = None
                    break
                else:
                    #Tratar mensagens recebidas por cada cliente
                    Server.messageBuffer[id - 1].append(data.decode())

            except:
                break
        conn.close()
    
    def send(player: int, message: str):
        ''' Função para enviar mensagem para apenas um cliente. '''
        if Server.clients[player]: #Caso a conexão seja None, a mensagem não deve ir
            Server.clients[player].send(str.encode(message+"#"))


    def send_others(indice: int, data: str):
        ''' Função para enviar mensagem para todos os outros clientes, exceto um. '''
        n_clients = len(Server.clients) 

        for i in range(n_clients):
            if i == indice: 
                continue

            Server.send(i, data)

    def send_all(data: str):
        ''' Função para enviar mensagem para todos os clientes. '''
        n_clients = len(Server.clients) 

        for i in range(n_clients):
            Server.send(i, data)
    
