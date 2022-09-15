import re
import os
import sys
import time
import random

class Menu:
    # Limpa a tela.
    def limpaTela():
        
        os.system('cls' if os.name == 'nt' else 'clear')

    ##
    # Funcoes de manipulacao do tabuleiro
    ##

    # Imprime estado atual do tabuleiro
    def imprimeTabuleiro(tabuleiro):

        # Limpa a tela
        Menu.limpaTela()

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
    
    
