import os
import sys
import time
import random

from _thread import *
from servidor import Server

##
# Funcoes uteis
##./

# Limpa a tela.
def limpaTela():

    os.system('cls' if os.name == 'nt' else 'clear')

##
# Funcoes de manipulacao do tabuleiro
##

# Imprime estado atual do tabuleiro
def imprimeTabuleiro(tabuleiro):

    # Limpa a tela
    limpaTela()

    # Imprime coordenadas horizontais
    dim = len(tabuleiro)
    Server.send_all("%      ")
    sys.stdout.write("     ")
    for i in range(dim):
        Server.send_all("% {0:2d} ".format(i))
        sys.stdout.write("{0:2d} ".format(i))

    sys.stdout.write("\n")
    Server.send_all("% \n")

    # Imprime separador horizontal
    sys.stdout.write("-----")
    Server.send_all("% -----")
    for i in range(dim):
        Server.send_all("% ---")
        sys.stdout.write("---")

    sys.stdout.write("\n")
    Server.send_all("% \n")

    for i in range(dim):

        # Imprime coordenadas verticais
        Server.send_all("% {0:2d} | ".format(i))
        sys.stdout.write("{0:2d} | ".format(i))

        # Imprime conteudo da linha 'i'
        for j in range(dim):

            # Peca ja foi removida?
            if tabuleiro[i][j] == '-':

                # Sim.
                Server.send_all("%  -")
                sys.stdout.write(" - ")

            # Peca esta levantada?
            elif tabuleiro[i][j] >= 0:

                # Sim, imprime valor.
                Server.send_all("% {0:2d} ".format(tabuleiro[i][j]))
                sys.stdout.write("{0:2d} ".format(tabuleiro[i][j]))
            else:

                # Nao, imprime '?'
                Server.send_all("%  ? ")
                sys.stdout.write(" ? ")

        Server.send_all("% \n")
        sys.stdout.write("\n")

# Cria um novo tabuleiro com pecas aleatorias. 
# 'dim' eh a dimensao do tabuleiro, necessariamente
# par.
def novoTabuleiro(dim):

    # Cria um tabuleiro vazio.
    tabuleiro = []
    for i in range(dim):

        linha = []
        for j in range(dim):

            linha.append(0)

        tabuleiro.append(linha)

    # Cria uma lista de todas as posicoes do tabuleiro. Util para
    # sortearmos posicoes aleatoriamente para as pecas.
    posicoesDisponiveis = []
    for i in range(dim):

        for j in range(dim):

            posicoesDisponiveis.append((i, j))

    # Varre todas as pecas que serao colocadas no 
    # tabuleiro e posiciona cada par de pecas iguais
    # em posicoes aleatorias.
    for j in range(int(dim / 2)):
        for i in range(1, dim + 1):

            # Sorteio da posicao da segunda peca com valor 'i'
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

            # Sorteio da posicao da segunda peca com valor 'i'
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

    return tabuleiro

# Abre (revela) peca na posicao (i, j). Se posicao ja esta
# aberta ou se ja foi removida, retorna False. Retorna True
# caso contrario.
def abrePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] < 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False

# Fecha peca na posicao (i, j). Se posicao ja esta
# fechada ou se ja foi removida, retorna False. Retorna True
# caso contrario.
def fechaPeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    elif tabuleiro[i][j] > 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False

# Remove peca na posicao (i, j). Se posicao ja esta
# removida, retorna False. Retorna True
# caso contrario.
def removePeca(tabuleiro, i, j):

    if tabuleiro[i][j] == '-':
        return False
    else:
        tabuleiro[i][j] = "-"
        return True

## 
# Funcoes de manipulacao do placar
##

# Cria um novo placar zerado.
def novoPlacar(nJogadores):

    return [0] * nJogadores

# Adiciona um ponto no placar para o jogador especificado.
def incrementaPlacar(placar, jogador):

    placar[jogador] = placar[jogador] + 1

# Imprime o placar atual.
def imprimePlacar(placar):

    nJogadores = len(placar)

    print("Placar:\n---------------------")
    for i in range(nJogadores):
        print("Jogador {0}: {1:2d}".format(i + 1, placar[i]))

##
# Funcoes de interacao com o usuario
#

# Imprime informacoes basicas sobre o estado atual da partida.
def imprimeStatus(tabuleiro, placar, vez):

        imprimeTabuleiro(tabuleiro)
        sys.stdout.write('\n')
        Server.send_all("% \n")

        imprimePlacar(placar)
        sys.stdout.write('\n')
        sys.stdout.write('\n')


        
        print("Vez do Jogador {0}.\n".format(vez + 1))

# Le um coordenadas de uma peca. Retorna uma tupla do tipo (i, j)
# em caso de sucesso, ou False em caso de erro.
def leCoordenada(dim, vez):
    Server.send(vez, "> \nEspecifique uma peca: ")

    #Esperando mensagem do servidor e contando tempo
    start = time.time()
    
    noMessage = False
    
    # 1 minuto para fazer jogada
    while len(Server.messageBuffer[vez]) == 0: 
        end = time.time()
        if (end-start) >= 60:
            noMessage = True
            break
        pass

    if Server.messageBuffer[vez][0] == None or noMessage:
        Server.send_others(vez, f"O Jogador {vez + 1} está ausente...\n\nFim de jogo.")
        return "Game Over"

    inp = Server.messageBuffer[vez].pop(0)
        
    try:
        i = int(inp.split(' ')[0])
        j = int(inp.split(' ')[1])
    except ValueError:

        erro = f"+ Coordenadas invalidas! Use o formato \"i j\" (sem aspas),\nonde i e j sao inteiros maiores ou iguais a 0 e menores que {dim}\n"
        Server.send(vez, erro)
        return False

    if i < 0 or i >= dim:

        erro = f"+ Coordenada i deve ser maior ou igual a zero e menor que {dim}\n"
        Server.send(vez, erro)
        return False

    if j < 0 or j >= dim:

        erro = f"+ Coordenada j deve ser maior ou igual a zero e menor que {dim}\n"
        Server.send(vez, erro)
        return False

    Server.send_others(vez, f"O Jogador {vez + 1} jogou {i} {j}...\n")
    return (i, j)

##
# Parametros da partida
##
def jogo():

    Server.start()
    # Tamanho (da lateral) do tabuleiro. NECESSARIAMENTE PAR E MENOR QUE 10!
    while True:
        Server.send(0,"> Informe o tamanho do tabuleiro (2, 4, 6 ou 8): ")
        print("Informe o tamanho do tabuleiro (2, 4, 6 ou 8): ")
        #Esperando mensagem do servidor
        while len(Server.messageBuffer[0]) == 0: pass

        dim = int(Server.messageBuffer[0].pop(0))
        print(dim)
        if dim in [2,4,6,8]:
            break
        Server.send(0,"> Valor inválido!\n")
        print("Valor inválido!\n")

    # Numero de jogadores
    Server.send(0, "> Indique o número total de jogadores: ")
    print("Informe o número total de jogadores: ")

    #Esperando mensagem do servidor
    while len(Server.messageBuffer[0]) == 0: pass

    nJogadores = int(Server.messageBuffer[0].pop(0))
    print(nJogadores)
    start_new_thread(Server.start_t,(nJogadores,))
    

    #Esperando jogadores se conectarem
    while(not Server.playersConnected): pass   

    # Numero total de pares de pecas
    totalDePares = dim**2 / 2

    ##
    # Programa principal
    ##

    # Cria um novo tabuleiro para a partida
    tabuleiro = novoTabuleiro(dim)


    # Cria um novo placar zerado
    placar = novoPlacar(nJogadores)

    # Partida continua enquanto ainda ha pares de pecas a 
    # casar.
    paresEncontrados = 0
    vez = 0
    while paresEncontrados < totalDePares:

        # Requisita primeira peca do proximo jogador
        while True:

            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)
            Server.send_others(vez, f"Vez do Jogador {vez + 1}.\n")
            Server.send(vez, "\nSua vez de jogar!\n")        

            # Solicita coordenadas da primeira peca.
            coordenadas = leCoordenada(dim, vez)
            if coordenadas == "Game Over":
                break

            if coordenadas == False:
                continue

            i1, j1 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i1, j1) == False:
                Server.send(vez, "+ Escolha uma peca ainda fechada!\n")
                continue

            break 

        if coordenadas == "Game Over":
            break

        # Requisita segunda peca do proximo jogador
        while True:

            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            # Solicita coordenadas da segunda peca.
            coordenadas = leCoordenada(dim, vez)
            if coordenadas == "Game Over":
                break
            if coordenadas == False:
                continue

            i2, j2 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i2, j2) == False:

                Server.send(vez, "+ Escolha uma peca ainda fechada!\n")
                continue

            break 

        if coordenadas == "Game Over":
            break
        # Imprime status do jogo
        imprimeStatus(tabuleiro, placar, vez)
        Server.send_all("\n\nPlacar:\n---------------------")
        for i in range(nJogadores):
            Server.send_all("Jogador {0}: {1:2d}".format(i + 1, placar[i]))
        Server.send_all("\n")


        print("Pecas escolhidas --> ({0}, {1}) e ({2}, {3})\n".format(i1, j1, i2, j2))
        Server.send_others(vez, f"Pecas escolhidas --> ({i1}, {j1}) e ({i2}, {j2})")

        # Pecas escolhidas sao iguais?
        if tabuleiro[i1][j1] == tabuleiro[i2][j2]:

            Server.send(vez, "Parabéns você pontuou! Agora, você joga novamente.\n")

            print("Pecas casam! Ponto para o jogador {0}.".format(vez + 1))
            Server.send_others(vez, f"Pecas casam! Ponto para o jogador {vez + 1}.\n")
            
            incrementaPlacar(placar, vez)
            paresEncontrados = paresEncontrados + 1
            removePeca(tabuleiro, i1, j1)
            removePeca(tabuleiro, i2, j2)

            time.sleep(5)
        else:
            Server.send(vez, "Pecas nao casam!\n")
            Server.send_others(vez, f"Pecas não casam! Acabou a vez do jogador {vez + 1}.\n")
            
            time.sleep(3)

            fechaPeca(tabuleiro, i1, j1)
            fechaPeca(tabuleiro, i2, j2)
            vez = (vez + 1) % nJogadores

    # Verificar o vencedor e imprimir
    pontuacaoMaxima = max(placar)
    vencedores = []
    for i in range(nJogadores):

        if placar[i] == pontuacaoMaxima:
            vencedores.append(i)

    if len(vencedores) > 1:

        sys.stdout.write("\nHouve empate entre os jogadores ")
        Server.send_all("% \nHouve empate entre os jogadores:")
        
        
        for i in vencedores:
            Server.send_all(f"% {i+1}")
            sys.stdout.write(str(i + 1) + ' ')

        Server.send_all(f"* \n\nFim de jogo.")
        sys.stdout.write(".\n\n")

    else:

        Server.send_others(vencedores[0], f"* Jogador {vencedores[0] + 1} foi o vencedor!\n")
        Server.send(vencedores[0], "* Você ganhou! Uhuuul!\n")
        print("\nJogador {0} foi o vencedor!\n".format(vencedores[0] + 1))

#Manter servidor rodando
while True:
    jogo()

    #Esperar jogadores se desconectarem
    time.sleep(1)

    #Preparar servidor para novo jogo
    Server.resetServerInfo()
    print("Novo jogo!")

