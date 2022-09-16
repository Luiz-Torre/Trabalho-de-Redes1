import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "localhost"  # IP local
PORT = 1332     # porta para conexão
s.bind((HOST, PORT))
s.listen()
print("antes")
conn, addr = s.accept()
print("depois")
