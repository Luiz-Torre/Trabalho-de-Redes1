import socket
from socket import socket as Socket
from _thread import *
import sys


class Server:

    HOST = "localhost"  # IP local
    PORT = 1331     # porta para conexão
    socket = None   # socket do servidor, sem valor atribuído
    clients = []    # lista de clientes conectados
    playersConnected = False


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

    def start_t(n_players: int): 
        ''' Thread criada para esperar N conexões com o servidor. '''
        while True:
            print("Aguardando jogadores...")

            conn, addr = Server.socket.accept()
            n_clients = len(Server.clients) 

            Server.clients.append(conn)
            print(f"{addr} está conectado.")

            #Manda para o player seu ID no servidor   
            conn.send(str.encode(f"id:{n_clients+1}"))

            start_new_thread(Server.client_t, (conn, n_clients+1))

            if n_clients + 1 >= n_players:
                print("Jogadores conectados.")
                Server.playersConnected = True
                break
                

    def client_t(conn: Socket, id: int):
        while True:
            try:
                data = conn.recv(4096) #conexao recebe

                if not data:
                    print("Player " + str(id) + " disconnected")
                    Server.clients[id - 1] = None
                    break
                else:
                    #Tratar mensagens recebidas por cada cliente
                    Server.send_others(id, data)
            except:
                break
        
        conn.close()

    def send_others(id: int, data: bytes):
        n_clients = len(Server.clients) 

        for i in range(n_clients):
            if i + 1 == id: continue

            Server.clients[i].send(data)