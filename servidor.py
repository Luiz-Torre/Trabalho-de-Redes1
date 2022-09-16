import socket
from socket import socket as Socket
from _thread import *
import sys


class Server:

    HOST = "localhost"  # IP local
    PORT = 1331     # porta para conexão
    socket = None   # socket do servidor, sem valor atribuído
    clients = []    # lista de clientes conectados


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

            if n_clients < n_players:   
                conn.send(str.encode(f"player:{n_clients+1}"))
                Server.clients.append(conn)
                print(f"{addr} está conectado.")
                start_new_thread(Server.client_t, (conn, n_clients+1))
            else:
                break

    def client_t(conn: Socket, id: int):
        while True:
            try:
                data = conn.recv(4096) #conexao recebe

                if not data:
                    print("Disconnected")
                    break
                else:
                    send_others(id, data)
            except:
                break
        
        conn.close()


    def send_others(id: int, data: bytes):
        n_clients = len(Server.clients) 

        for i in range(1, n_clients+1):
            if i == id: pass

            print(i)
            other.send(data)


Server.start(5)

while True:
    pass