# %% Importações

from copy import deepcopy
import os
import pickle
import sys
from matplotlib import markers

from tqdm import tqdm
import numpy as np
import scipy.io as io
import pandas as pd
import geopy.distance  # gps para distância

from dtwalign import dtw

import matplotlib.pyplot as plt

# %% Carregando os dados

path = r'C:\Users\vinic\python_projects\monitoracao_project\dados_parquet'

ace_data = pd.read_parquet(path+r'\LRV4306_acc-001.parquet')
gps_data = pd.read_parquet(path+r'\LRV4306_gps.parquet')
gps_reference_in = pd.read_csv(path+r'\region5_inbound.csv', header=None)
gps_reference_out = pd.read_csv(path+r'\region5_outbound.csv', header=None)


# %% Funções

# Dynamic time warping

def DynamicTimeWarping(referencia, gps, plot=False):
    # retorna os vetores alinhados
    # https://dtwalign.readthedocs.io/en/latest/tutorial.html

    res = dtw(gps, referencia)
    gps_novo = gps[res.get_warping_path(target="query")]

    if plot:

        plt.plot(gps, label='GPS antigo')
        plt.plot(referencia, label='Referencia')
        plt.plot(gps_novo, label='GPS alinhado')
        plt.legend()
        plt.show()

    return gps_novo


# Transformando coordenadas em distância

def Distancias(coordenadas):
    # retorna o vetor de distâncias dada determinada data, número de passagens e etc

    n = len(coordenadas.iloc[:, 0])
    dists = []
    for i in range(n-1):
        coords_1 = (coordenadas.iloc[i, 0], coordenadas.iloc[i, 1])
        coords_2 = (coordenadas.iloc[i+1, 0], coordenadas.iloc[i+1, 1])
        dists.append(geopy.distance.geodesic(coords_1, coords_2).km)

    return np.asarray(dists)


# Fazendo o upsampling
def Interpolador(distancias, n_final):
    # n_final = tamanho final do vetor
    # mult = número a ser adicionado em cada intervalo
    # caso não tenha o número entre intervalos, só o número a ser alcançado no final
    n_inicial = len(distancias)
    mult = int(round((n_final-n_inicial)/(n_inicial-1)))
    distancias_nova = []
    for i in tqdm(range(n_inicial-1)):
        a = (distancias[i+1]-distancias[i])/(mult+1)
        for j in range(mult+1):
            distancias_nova.append(a*j+distancias[i])

    distancias_nova.append(distancias[-1])

    return distancias_nova, mult


def AntiInterpolador(distancias_nova, mult):
    distancias_antiga = []
    n = len(distancias_nova)
    for i in range(n):
        if i % (mult+1) == 0:
            try:
                distancias_antiga.append(distancias_nova[i])
            except:
                distancias_antiga.append(distancias_nova.iloc[i])
    return distancias_antiga


# %% Carregando os dados por datas, n_passagens, direcao

# O que devemos fazer?

# valores de gps
# valores corrigidos de gps
# definir a distância
# função(distância, aceleração)
# machine learning


datas = set(gps_data.loc[:, 'date'])
n_passagens = set(gps_data.loc[:, 'daily_passing'])
direcoes = set(gps_data.loc[:, 'running_direction'])

"""p = list(datas)[0]
q = list(n_passagens)[0]
r = list(direcoes)[0]"""

for p in datas:
    for q in n_passagens:
        for r in direcoes:

            valor_gps = gps_data.loc[(gps_data.loc[:, [
                                      'date', 'daily_passing', 'running_direction']] == [p, q, r]).all(axis=1), :]
            valor_gps_corrigido = deepcopy(valor_gps)

            if len(valor_gps.iloc[:, 0]) > 50:
                if r == 1:

                    y = gps_reference_out.iloc[:, 2]
                    x, mult = np.asarray(Interpolador(
                        list(valor_gps.iloc[:, 0]), len(y)))
                    x = np.asarray(x)
                    z = DynamicTimeWarping(x, y, True)
                    valor_gps_corrigido.iloc[:, 0] = AntiInterpolador(z, mult)

                    y = gps_reference_out.iloc[:, 1]
                    x, mult = np.asarray(Interpolador(
                        list(valor_gps.iloc[:, 1]), len(y)))
                    x = np.asarray(x)
                    z = DynamicTimeWarping(x, y, True)
                    valor_gps_corrigido.iloc[:, 1] = AntiInterpolador(z, mult)

                else:
                    y = gps_reference_in.iloc[:, 2]
                    x, mult = np.asarray(Interpolador(
                        list(valor_gps.iloc[:, 0]), len(y)))
                    x = np.asarray(x)
                    z = DynamicTimeWarping(x, y, True)
                    valor_gps_corrigido.iloc[:, 0] = AntiInterpolador(z, mult)

                    y = gps_reference_in.iloc[:, 1]
                    x, mult = np.asarray(Interpolador(
                        list(valor_gps.iloc[:, 1]), len(y)))
                    x = np.asarray(x)
                    z = DynamicTimeWarping(x, y, True)
                    valor_gps_corrigido.iloc[:, 1] = AntiInterpolador(z, mult)

                distancias = Distancias(valor_gps_corrigido)

                valor_ace = ace_data.loc[(ace_data.loc[:, [
                                          'date', 'daily_passing', 'running_direction']] == [p, q, r]).all(axis=1), :]

                mult = len(ace_data.iloc[:, 0])
                distancias_up = Interpolador(distancias, mult)

                break

                # Tratar dados

                # treinar modelo de machine learning


# %% teste


datas = set(gps_data.loc[:, 'date'])
n_passagens = set(gps_data.loc[:, 'daily_passing'])
direcoes = set(gps_data.loc[:, 'running_direction'])

p = list(datas)[0]
q = list(n_passagens)[0]
r = list(direcoes)[0]


valor_gps = gps_data.loc[(gps_data.loc[:, [
                          'date', 'daily_passing', 'running_direction']] == [p, q, r]).all(axis=1), :]
valor_gps_corrigido = deepcopy(valor_gps)

if len(valor_gps.iloc[:, 0]) > 50:
    if r == 1:

        y = gps_reference_out.iloc[:, 2]
        x = np.asarray(Interpolador(
            list(valor_gps.iloc[:, 0]), len(list(y)))[0])
        valor_gps_corrigido.iloc[:, 0] = DynamicTimeWarping(x, y, True)

        y = gps_reference_out.iloc[:, 1]
        x = np.asarray(Interpolador(
            list(valor_gps.iloc[:, 1]), len(list(y)))[0])
        valor_gps_corrigido.iloc[:, 1] = DynamicTimeWarping(x, y)

    else:
        y = gps_reference_in.iloc[:, 2]
        x = np.asarray(Interpolador(
            list(valor_gps.iloc[:, 0]), len(list(y)))[0])
        valor_gps_corrigido.iloc[:, 0] = DynamicTimeWarping(x, y)

        y = gps_reference_in.iloc[:, 1]
        x = np.asarray(Interpolador(
            list(valor_gps.iloc[:, 1]), len(list(y)))[0])
        valor_gps_corrigido.iloc[:, 1] = DynamicTimeWarping(x, y)

    distancias = Distancias(p, q, r, valor_gps_corrigido)

    mult = round(len(gps_data.iloc[:, 0])/len(ace_data.iloc[:, 0]))
    distancias_up = Interpolador(distancias, mult)

    # Tratar dados

    # treinar modelo de machine learning


# %% Teste função dtw

#x = np.array([0, 2, 3, 4, 2])
#teste_inter = Interpolador(x, 3)
#y = np.array([2, 3, 2])

#x = gps_reference_out.iloc[:, 2]
#y = np.asarray(Interpolador(list(valor_gps.iloc[:, 0]), len(list(x))))
z = DynamicTimeWarping(x, y, True)

plt.plot(x, label='GPS antigo', markers='x')
plt.plot(y, label='Referencia', markers='y')
plt.plot(z, label='GPS alinhado', markers='s')
plt.legend()
plt.show()
# %%
