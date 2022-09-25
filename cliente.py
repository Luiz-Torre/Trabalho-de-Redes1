import socket
import os

from servidor import Server


class Client():
    def __init__(self):
        ''' Inicia o Cliente '''
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 1331
        self.addr = (self.server, self.port)
        self.id = self.connect() 
        self.last_response = ""

    def connect(self):
        ''' Realiza a conexão com o servidor '''
        try:
            self.client.connect(self.addr)
            return self.client.recv(1024).decode().split(":")[1] #id
        except:
            print("Failed to connect.")
            pass

    def send(self, msg: str):
        ''' Realiza o envio de mensagens para o servidor '''
        try:
            self.client.send(msg.encode())
        except socket.error as e:
            print(e)

    def receive_messages(self):
        ''' Realiza o recebimento das mensagens, processa e trata '''
        print("Seja bem vindo ao jogo da Memória da UFF. Caso sem algum momento deseje sair, digite SAIR na sua vez!\n\nAguarde os outros jogadores se conectarem...")
        while True:
            data = self.client.recv(1024)
            self.last_response = data.decode()

            #Processar mensagens
            messages = self.last_response.split("#")[:-1]
            os.system('cls||clear')
            
            #Tratar mensagens
            for m in messages:
                type_of_m = m[0] #tipo da mensagem

                #Se for uma ação
                if type_of_m == ">":
                    #Mandar coordenadas
                    coordenadas = input(m[2:])
                    self.send(coordenadas)
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
                    return # encerra o programa
                elif type_of_m == "!":
                    print("\U0001f499\U0001f499 Que pena que você está saindo. Até um próximo jogo! \U0001f499 \U0001f499")
                    self.client.close()
                    return # encerra o programa
                else:
                    print(m)


    def close(self):
        ''' Fecha a conexão com o servidor '''
        self.client.close()

c = Client()
c.receive_messages()



