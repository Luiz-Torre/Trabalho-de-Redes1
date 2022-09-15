import socket
from _thread import *
import sys

server = "localhost"
port = 1330

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)

print("Wating connection...")

connections = []
def threadead_client(conn, id):
    while True:
        try:
            data = conn.recv(4096)#conexao recebe

            if not data:
                print("Disconnected")
                break
            
            if(id == 1):#se o id é 1, então tem que mandar pra conexao 2 e viceversa
                print("sendto: ", id)
                connections[1].send(data)
            else:
                print("sendto: ", id)
                connections[0].send(data)

        except:
            break
    
    conn.close()

n_player = 1
while True:
    conn,addr = s.accept()
    n_connections = len(connections) 

    if(n_connections < 10):
        conn.send(str.encode(f"player:{n_connections+1}"))
        connections.append(conn)
        print('conected to: ', addr)
        start_new_thread(threadead_client, (conn, n_connections+1,))