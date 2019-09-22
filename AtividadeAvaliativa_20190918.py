""" Regressão Linear """
from random import randint
import matplotlib.pyplot as plt
import csv
import math

class Regrassao:

    def run(self):
        dados = []
        with open("AnaliseEstudo.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            for row in csv_reader:
                if row[0] != "Idade":
                    media = (int(row[3]) + int(row[4]) + int(row[5])) / 3 
                    aux = {
                        "Idade": row[0],
                        "TempoEstudo": row[1],
                        "Faltas":row[2],
                        "MediaProvas": media
                    }
                    dados.append(aux)
        N = len(dados)
        for tipo in ["Idade", "TempoEstudo", "Faltas"]:
            self.get_modelo(dados, tipo, N)

    def get_modelo(self, dados, tipo, N):
        s_dados = self.split_dados(dados, tipo)
        base_treino, base_teste = self.split_bases(s_dados, N)
        B0, B1 = self.regressao_linear(base_treino, tipo)
        xs = [d[0] for d in s_dados]
        ys_r = [(B0 + (d[0] * B1)) for d in s_dados]
        desvio = self.calc_desvio(base_teste, B0, B1)
        # self.testa_funcao(B0,B1,base_teste)
        print("Desvio padrão: " + str(desvio))
        plt.title('Média das Provas x ' + tipo )
        plt.xlabel(tipo.title())
        plt.ylabel('Média das provas')
        plt.plot(xs, ys_r)
        plt.show()

    def calc_desvio(self, base_teste, B0, B1):
        """ Calcula o desvio padrão de acordo com os resultados encontrados na base de teste 
        * Não tenho certeza se está correto
         """
        desvio = 0
        for d in base_teste:
            y = d[1]
            fx = (B0 + (d[0] * B1))
            desvio += (y - fx) ** 2
        return desvio

    def regressao_linear(self, b_treino, tipo):
        """ Monta o modelo usando a base de treino, retornando o valor de B0 e de B1"""
        N = len(b_treino)
        s_x = self.somat(b_treino, 'x')
        s_y = self.somat(b_treino, 'y')
        s_xy = self.somat(b_treino, 'xy')
        s_x2 = self.somat(b_treino, 'x2')
        B1 = ((s_x * s_y) - (N * s_xy)) / ((s_x ** 2) - (N * s_x2))
        B0 = (s_y - (B1 * s_x))/ N
        print(tipo + ": y = " + str(B0) + " + " + str(B1) + "x")
        return B0, B1
    
    def testa_funcao(self, B0, B1, dados_para_teste):
        """ Testa a função printando o (x, y, f(x)): para verificar se o valor de saída do modelo é próximo ao real"""
        for t in dados_para_teste:
            print("x: " + str(t[0]) + ", y: "+ str(t[1]) + ", f(x): "+ str(B0 + (t[0] * B1)))

    def somat(self, lista_de_numeros, tipo):
        """" Realiza o somatório """
        numeros = []
        for t in lista_de_numeros:
            if tipo == 'x':
                a = t[0]
            elif tipo == 'y':
                a = t[1]
            elif tipo == 'xy':
                a = t[0] * t[1]
            elif tipo == 'x2':
                a = t[0] ** 2
            else:
                a = 1
                print('Erro')
            numeros.append(a)
        return sum(numeros)
            
    def split_bases(self,dados, N):
        """ Separa a lista de dados em base de treino e de testes """
        posicoes_para_treino = []
        while (len(posicoes_para_treino) < round(N * 0.7)):
            posicao = randint(0, N - 1)
            if posicao not in posicoes_para_treino:
                posicoes_para_treino.append(posicao)
        dados_para_treino = [dados[p] for p in posicoes_para_treino]
        dados_para_teste = [dados[p] for p in range(len(dados)) if p not in posicoes_para_treino]
        # print("Base para treino: " + str(dados_para_treino))
        # print("Base para teste: " + str(dados_para_teste))
        return dados_para_treino, dados_para_teste
   
    def split_dados(self, dados, tipo):
        """ Pega o x de acordo com o tipo do modelo a ser treinado """
        resultados = []
        for item in dados:
            if tipo == "Idade":
                x = item.get("Idade")
            elif tipo == "TempoEstudo":
                x = item.get("TempoEstudo")
            elif tipo == "Faltas":
                x = item.get("Faltas") 
            y = item.get("MediaProvas")
            resultados.append((int(x), int(y)))
        return resultados

if __name__ == "__main__":
    reg = Regrassao()
    reg.run()