# %% Importações

from copy import deepcopy
import os
import pickle
import sys

from tqdm import tqdm
import numpy as np
import scipy.io as io
import pandas as pd
import geopy.distance # gps para distância
# from dtw import * # dynamic time warping

from dtwalign import dtw

import matplotlib.pyplot as plt

#%% Carregando os dados

path = r'C:\Users\vinic\python_projects\monitoracao_project\dados_parquet'

ace_data = pd.read_parquet(path+r'\LRV4306_acc-001.parquet')
gps_data = pd.read_parquet(path+r'\LRV4306_gps.parquet')
gps_reference_in = pd.read_csv(path+r'\region5_inbound.csv', header=None)
gps_reference_out = pd.read_csv(path+r'\region5_outbound.csv', header=None)



#%% Funções

# Dynamic time warping

def DynamicTimeWarping(referencia, gps):
    #retorna os vetores alinhados
    # https://dtwalign.readthedocs.io/en/latest/tutorial.html

    res = dtw(gps, referencia)
    return gps[res.get_warping_path(target="query")]
    


# Transformando coordenadas em distância

def Distancias(data, n_passagens, direcao, gps_data):
    # retorna o vetor de distâncias dada determinada data, número de passagens e etc

    #data = '20130102' # definir as datas dps
    coordenadas = (gps_data.loc['Data', 'N Passagens', 'Direcao']==\
        (data, n_passagens, direcao)).iloc[:, [0, 1]] # matriz(n,2) com os valores de coordenadas de determinado dataset

    n = len(coordenadas.iloc[:,0])
    dists = np.zeros(n-1,1)
    for i in range(len(coordenadas)-1):
        coords_1 = (coordenadas[i, 0], coordenadas[i, 1])
        coords_2 = (coordenadas[i+1, 0], coordenadas[i+1, 1])
        dists[i] = geopy.distance.geodesic(coords_1, coords_2).km

    return dists



# Velocidade

def Velocidade(distancias, tempos):
    velocidades = distancias/tempos
    return velocidades



# Fazendo o upsampling
def InterpoladorVelocidade(distancias, mult):
    # mult = len(distancias_nova)/len(distancias), len(distancias_nova)>len(distancias)
    n = len(distancias)-1
    distancias_nova = []
    for i in range(n):
        a = (distancias[i+1]-distancias[i])/mult
        for j in range(mult):
            distancias_nova.append(a*j)+distancias[i]
    
    return distancias_nova



# %% Teste DWT

"""np.random.seed(1234)
# generate toy data
x = np.sin(2 * np.pi * 3.1 * np.linspace(0, 1, 101))
x += np.random.rand(x.size)
y = np.sin(2 * np.pi * 3 * np.linspace(0, 1, 120))
y += np.random.rand(y.size)

plt.plot(x, label="query")
plt.plot(y, label="reference")
plt.legend()
plt.ylim(-1, 3)
plt.show()

res = dtw(x,y)

#x_path = res.path[:, 0]
#y_path = res.path[:, 1]

x_warping_path = res.get_warping_path(target="query")
plt.plot(x[x_warping_path], label="aligned query to reference")
plt.plot(y, label="reference")
plt.legend()
plt.ylim(-1, 3)"""



#%% Carregando os dados por datas, n_passagens, direcao

# O que devemos fazer?

# valores de gps
# valores corrigidos de gps
# definir a distância
# função(distância, aceleração)
# machine learning


datas = set(gps_data.loc[:,'date'])
n_passagens = set(gps_data.loc[:,'daily_passing'])
direcoes = set(gps_data.loc[:,'running_direction'])

for p in datas:
    for q in n_passagens:
        for r in direcoes:
            
            valor_gps = (gps_data.loc[:,['date', 'daily_passing', 'running_direction']]==[p, q, r])
            valor_gps_corrigido = deepcopy(valor_gps)

            if direcoes == 1:
                valor_gps_corrigido.iloc[:,0] = \
                    DynamicTimeWarping(gps_reference_out.iloc[:, 2], valor_gps[:, 0])
    
                valor_gps_corrigido.iloc[:,1] = \
                    DynamicTimeWarping(gps_reference_out.iloc[:, 1], valor_gps[:, 1])

            else:
                valor_gps_corrigido.iloc[:,0] = \
                    DynamicTimeWarping(gps_reference_in.iloc[:, 2], valor_gps[:, 0])
    
                valor_gps_corrigido.iloc[:,1] = \
                    DynamicTimeWarping(gps_reference_in.iloc[:, 1], valor_gps[:, 1])
            
            
            distancias = Distancias(p, q, r, valor_gps_corrigido)

            mult = round(len(gps_data.iloc[:, 0])/len(ace_data.iloc[:,0]))
            distancias_up = InterpoladorVelocidade(distancias, mult)            
                    
                        # Tratar dados

                        # treinar modelo de machine learning


#%% O que devemos fazer

# valores de gps
# valores corrigidos de gps
# definir a distância
# função(distância, aceleração)
# machine learning