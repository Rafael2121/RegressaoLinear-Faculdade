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
        idade = self.get_informacoes(dados,"Idade", N)
        tempo_estudo = self.get_informacoes(dados, "TempoEstudo", N)
        faltas = self.get_informacoes(dados, "Faltas", N)

    def get_informacoes(self, dados, tipo, N):
        dados = self.get_dados(dados, tipo)
        base_treino, base_teste = self.get_base_treino(dados, N)
        B0, B1 = self.regressao_linear(base_treino, tipo)
        xs = [d[0] for d in dados]
        # ys = [d[1] for d in dados]
        ys_r = [(B0 + (d[0] * B1)) for d in dados]
        desvio = self.get_desvio(base_teste, B0, B1)
        self.testa_funcao(B0,B1,base_teste)
        print("Desvio padrão: " + str(desvio))
        plt.title('Média das Provas x ' + tipo )
        plt.xlabel(tipo.title())
        plt.ylabel('Média das provas')
        plt.plot(xs, ys_r)
        plt.show()
        return True

    def get_desvio(self, base_teste, B0, B1):
        desvio = 0
        for d in base_teste:
            y = d[1]
            fx = (B0 + (d[0] * B1))
            desvio += (y - fx) ** 2
        return desvio
    
    def get_dados(self, dados, tipo):
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
        
    def regressao_linear(self, b_teste, tipo):
        N = len(b_teste)
        s_x = self.somat(b_teste, 'x')
        s_y = self.somat(b_teste, 'y')
        s_xy = self.somat(b_teste, 'xy')
        s_x2 = self.somat(b_teste, 'x2')
        B1 = ((s_x * s_y) - (N * s_xy)) / ((s_x ** 2) - (N * s_x2))
        B0 = (s_y - (B1 * s_x))/ N
        print(tipo + ": y = " + str(B0) + " + " + str(B1) + "x")
        return B0, B1
    
    def testa_funcao(self, B0, B1, dados_para_teste):
        for t in dados_para_teste:
            y = B0 + (t[0] * B1)
            print("x: " + str(t[0]) + ", y: "+ str(t[1]) + ", f(x): "+ str(y))

    def somat(self,lista_de_numeros, tipo):
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
            
    def get_base_treino(self,dados, N):
        posicoes_para_treino = []
        while (len(posicoes_para_treino) < round(N * 0.7)):
            posicao = randint(0, N - 1)
            if posicao not in posicoes_para_treino:
                posicoes_para_treino.append(posicao)
        dados_para_treino = [dados[posicao] for posicao in posicoes_para_treino]
        dados_para_teste = [dados[posicao_do_dado] for posicao_do_dado in range(len(dados)) if posicao_do_dado not in posicoes_para_treino]
        
        # print("Base para treino: " + str(dados_para_treino))
        # print("Base para teste: " + str(dados_para_teste))
        return dados_para_treino, dados_para_teste

if __name__ == "__main__":
    reg = Regrassao()
    reg.run()