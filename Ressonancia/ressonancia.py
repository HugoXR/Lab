import numpy as np
from PyGnuplot import gp

"""
    Script para tratar os dados do experimento de ressonancia, calculando,
    a partir da tensao no resistor para cada valor de frequencia, a corrente
    em funcao da frequencia, encontrando a frequencia de ressonancia
    (frequencia_max) e, atraves de uma regressao obtendo o fator de qualidade Q
    do circuito RLC.

    O Arquivo lido deve ter a frequencia na primeira coluna e a tensao no
    resistor na segunda coluna, separados por vírgula, os dados de entrada
    devem ser escritos com ponto flutuante.

    O Script retornara um arquivo chamado "Dados_Resistor_Tratados.txt", com
    a frequencia e as correspodentes correntes. Alem deste o mesmo retornara o
    arquivo "fit.log" com o log do fit realizado para obter a curva, e o
    "fit_parameters.txt" para coletar os dados do fit. O ultimo arquivo gerado
    é o "grafico_ressonancia.png" com um grafico, feito atraves do gnuplot, com
    o fit da curva e os dados necessarios para a analise.
"""

# Dados de entrada
# ----------------------------------------------------------------------
arquivo = input("Nome do arquivo com os dados (.txt): ")
resistencia = float(input("Valor da resistencia: "))
capacitancia = float(input("Valor da capacitancia: "))
indutancia = float(input("Valor da indutancia: "))
Q_previsto = input("Valor de Q Previsto: ")
w_previsto = input("Valor da frequencia de ressonancia previsto: ")
A_previsto = input("Valor da corrente max prevista: ")
# ----------------------------------------------------------------------
# Matriz com os dados
# -----------------------------------------
dados = np.loadtxt(arquivo, delimiter=",")
# ------------------------------------------
# Separando os dados
# ------------------------------------------
frequencia = dados[:,0]
tensao_r = dados[:,1]
# ------------------------------------------
# Calculando as reatancias
# ----------------------------------------------------------
reatancia_capacitiva = 1/(2*np.pi*frequencia*capacitancia)
reatancia_indutiva = 2*np.pi*frequencia*indutancia
# ------------------------------------------------------------
# Concatenando os dados da frequencia com a corrente
# ----------------------------------------------------------------------------
dados_tratados_r = np.stack((frequencia, tensao_r/resistencia), axis=1)
# ----------------------------------------------------------------------------
# Salvando dados em um arquivo
# ----------------------------------------------------------------------------
np.savetxt("Dados_Resistencia_Tratados.txt", dados_tratados_r, delimiter=",")
# ----------------------------------------------------------------------------
# Obtendo a frequencia de maxima corrente e a corrente maxima
# ----------------------------------------------------------------------------
frequencia_max = float(frequencia[np.where(tensao_r == np.max(tensao_r))])
corrente_max = float(np.max(dados_tratados_r[:,1]))
# ---------------------------------------------------------------------------

# Gnuplot
# * ---------------------------------------------------- *
g = gp()

# Configuracoes iniciais no gnuplot
# -------------------------------------------------------
g.c('set encoding utf8')
g.c('set terminal png size 750,500')
g.c('set datafile separator ","')
g.c('set yrange[0:'+str(corrente_max*2)+']')
# -------------------------------------------------------
# Fitando curva
# -----------------------------------------------------------------------
g.c('I(x) = A/(sqrt(1 + (Q**2)*(x/w - w/x)**2))')
g.c('A = '+A_previsto)
g.c('w = '+w_previsto)
g.c('Q = '+Q_previsto)
g.c('fit [x=0:'+str(frequencia[-1])+'] I(x) "Dados_Resistencia_Tratados.txt" via Q,w,A')
# -----------------------------------------------------------------------
# Coletando dados do fit
# ---------------------------------------------------
g.c('set print "fit_parameters.txt"')
g.c('print Q,Q_err')
g.c('print A,A_err')
g.c('print w,w_err')
g.c('set print')
Q,A,w = '', '', ''
with open("fit_parameters.txt") as fit:
    Q = fit.readline()
    A = fit.readline()
    w = fit.readline()
# ------------------------------------------------------------------
# Tratando os dados obtidos no fit
# -------------------------------------------------------------------
Q_matriz = Q.strip("\n").split(" ")
Q = Q_matriz[0]
Q_err = Q_matriz[1]

for value in Q_err:
    if(value != '0' and value != '.'):
        pos = Q_err.find(value)
        break

if(pos != 0):
    Q_f = (Q.split(".")[0])+'.'+((Q.split(".")[1])[0:pos-1])
    Q_err = Q_err[0:pos+1]
elif (pos == 0 and Q_err[-4:-3] != "e"):
    Q_f = (Q.split(".")[0])
    Q_err = Q_err[0:pos+1]
else:
    pos_f = int(Q_err[-2:])
    if(Q_err[-3:-2] == "-"):
        Q_f = (Q.split(".")[0])+"."+((Q.split("."))[1])[:pos_f]
        Q_err = Q_err[0:pos+1]+Q_err[-4:]
    else:
        Q_f = (Q.split(".")[0])[:pos_f]
        Q_err = Q_err[0:pos+1]+Q_err[-4:]

A_matriz = A.strip("\n").split(" ")
A = A_matriz[0]
A_err = A_matriz[1]

for value in A_err:
    if (value != '0' and value != '.'):
        pos = A_err.find(value)
        break


if(pos != 0):
    A_f = (A.split(".")[0])+'.'+((A.split(".")[1])[0:pos-1])
    A_err = A_err[0:pos+1]
elif (pos == 0 and A_err[-4:-3] != "e"):
    A_f = (A.split(".")[0])
    A_err = A_err[0:pos+1]
else:
    pos_f = int(A_err[-2:])
    if(A_err[-3:-2] == "-"):
        A_f = (A.split(".")[0])+"."+((A.split("."))[1])[:pos_f]
        print(A_f)
        A_err = A_err[0:pos+1]+A_err[-4:]
    else:
        A_f = (A.split(".")[0])[:pos_f]
        A_err = A_err[0:pos+1]+A_err[-4:]


w_matriz = w.strip("\n").split(" ")
w = w_matriz[0]
w_err = w_matriz[1]

for value in w_err:
    if (value != '0' and value != '.'):
        pos = w_err.find(value)
        break


if(pos != 0):
    w_f = (w.split(".")[0])+'.'+((w.split(".")[1])[0:pos-1])
    w_err = w_err[0:pos+1]
elif (pos == 0 and w_err[-4:-3] != "e"):
    w_f = (w.split(".")[0])
    w_err = w_err[0:pos+1]
else:
    pos_f = int(w_err[-2:])
    if(Q_err[-3:-2] == "-"):
        w_f = (w.split(".")[0])+"."+((w.split("."))[1])[:pos_f]
        w_err = w_err[0:pos+1]+w_err[-4:]
    else:
        w_f = (w.split(".")[0])[:pos_f]
        w_err = w_err[0:pos+1]+w_err[-4:]
# --------------------------------------------------------------------

# Configurando e Plotando Graficos
# ----------------------------------------------------------------------------
g.c('set grid')
g.c('set xlabel "f (Hz)"')
g.c('set ylabel "I (A)"')
g.c('set title "Dados da Ressonância no Circuito RLC"')
g.c('set output "grafico_ressonancia.png"')
g.c('x = '+str(frequencia_max)+'')
g.c('set arrow from '+str(frequencia_max)+',0 to '+str(frequencia_max)+','+str(corrente_max*2)+'nohead lt 3')
g.c('plot "Dados_Resistencia_Tratados.txt" t "Dados do Resistor",I(x) t "\\n\\n\\n\\n\\n\\n\\n\\n\\nQ ='+Q_f+'+/-'+Q_err+'\\n\\nI_{max} =('+A_f+'+/-'+A_err+') A\\n\\nw = ('+w_f+'+/-'+w_err+')Hz", 1/0 t "f = '+str(frequencia_max)+'Hz" lt 3')
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
