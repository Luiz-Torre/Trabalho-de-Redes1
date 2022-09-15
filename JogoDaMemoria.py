import re
import os
import sys
import time
import random
import menu
##
# Funcoes uteis
##
class JogoDaMemoria():
    
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

        print("Placar:")
        print("---------------------")
        for i in range(nJogadores):
            print("Jogador {0}: {1:2d}".format(i + 1, placar[i]))

    ##
    # Funcoes de interacao com o usuario
    #

    # Imprime informacoes basicas sobre o estado atual da partida.
    def imprimeStatus(tabuleiro, placar, vez):

            menu.Menu.imprimeTabuleiro(tabuleiro)
            sys.stdout.write('\n')

            menu.Menu.imprimePlacar(placar)
            sys.stdout.write('\n')
            sys.stdout.write('\n')

            print("Vez do Jogador {0}.\n".format(vez + 1))

    # Le um coordenadas de uma peca. Retorna uma tupla do tipo (i, j)
    # em caso de sucesso, ou False em caso de erro.
    def leCoordenada(dim):

        inp = input("Especifique uma peca: ")

        try:
            i = int(inp.split(' ')[0])
            j = int(inp.split(' ')[1])
        except ValueError:
            print("Coordenadas invalidas! Use o formato \"i j\" (sem aspas),")
            print("onde i e j sao inteiros maiores ou iguais a 0 e menores que {0}".format(dim))
            input("Pressione <enter> para continuar...")
            return False

        if i < 0 or i >= dim:

            print("Coordenada i deve ser maior ou igual a zero e menor que {0}".format(dim))
            input("Pressione <enter> para continuar...")
            return False

        if j < 0 or j >= dim:

            print("Coordenada j deve ser maior ou igual a zero e menor que {0}".format(dim))
            input("Pressione <enter> para continuar...")
            return False

        return (i, j)

    ##
    # Parametros da partida
    ##

    # Tamanho (da lateral) do tabuleiro. NECESSARIAMENTE PAR E MENOR QUE 10!
    while True:
        dim = int(input("Informe o tamanho do tabuleiro (2, 4, 6 ou 8): "))
        if dim in [2,4,6,8]:
            break
        print("Valor inválido!\n")

    # Numero de jogadores
    nJogadores = int(input("Informe o número de jogadores: "))

    # Numero total de pares de pecas
    totalDePares = dim**2 / 2

    ##
    # Programa principal
    ##

    # Cria um novo tabuleiro para a partida
    tabuleiro = menu.Menu.novoTabuleiro(dim)

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

            # Solicita coordenadas da primeira peca.
            coordenadas = leCoordenada(dim)
            if coordenadas == False:
                continue

            i1, j1 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i1, j1) == False:

                print("Escolha uma peca ainda fechada!")
                input("Pressione <enter> para continuar...")
                continue

            break 

        # Requisita segunda peca do proximo jogador
        while True:

            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            # Solicita coordenadas da segunda peca.
            coordenadas = leCoordenada(dim)
            if coordenadas == False:
                continue

            i2, j2 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i2, j2) == False:

                print("Escolha uma peca ainda fechada!")
                input("Pressione <enter> para continuar...")
                continue

            break 

        # Imprime status do jogo
        imprimeStatus(tabuleiro, placar, vez)

        print("Pecas escolhidas --> ({0}, {1}) e ({2}, {3})\n".format(i1, j1, i2, j2))

        # Pecas escolhidas sao iguais?
        if tabuleiro[i1][j1] == tabuleiro[i2][j2]:

            print("Pecas casam! Ponto para o jogador {0}.".format(vez + 1))
            
            incrementaPlacar(placar, vez)
            paresEncontrados = paresEncontrados + 1
            removePeca(tabuleiro, i1, j1)
            removePeca(tabuleiro, i2, j2)

            time.sleep(5)
        else:

            print("Pecas nao casam!")
            
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

        sys.stdout.write("Houve empate entre os jogadores ")
        for i in vencedores:
            sys.stdout.write(str(i + 1) + ' ')

        sys.stdout.write("\n")

    else:

        print("Jogador {0} foi o vencedor!".format(vencedores[0] + 1))


