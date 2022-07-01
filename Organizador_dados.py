""" Organiza os dados da região 5 em 4 DataFrames (2 para o LRV4306 e 2 para o LRV4313, sendo 1 para a aceleração e 1 para gps), 
onde cada coluna é uma característica de acordo com as seguintes características:


-----------------------------------------------------------------------------------------
GPS files naming rules
-----------------------------------------------------------------------------------------

{file#}_{date}_{root index}_{daily passing#}_{region#}_{running direction}.mat

running direction: 1 - outbound
		   2 - inbound

-----------------------------------------------------------------------------------------
Acceleration files naming rules
-----------------------------------------------------------------------------------------

{file#}_{date}_{root index}_{daily passing#}_{region#}_{running direction}_{sensor channel}.mat

running direction: 1 - outbound
		   2 - inbound

 """ 


"""
Serão criados 4 Datasets, cada um correspondente aos trens e aos tipos de dados:

LRV4306_Acelleration
LRV4306_GPS

LRV4313_Acelleration
LRV4313_GPS

Cada um terá 4 índices: date, daily passing, running direction, sensor channel
Tendo como resposta 1 colunas: value (valor numérico das colunas)
"""


import h5py
import numpy as np
import scipy.io
from os import listdir
from os import mkdir
import pandas as pd
import matplotlib.pyplot as plt

"""Pasta de origem dos dados e pasta de destino para os dados trabalhados"""
path_sources = r'C:\Users\vinic\python_projects\monitoracao_project\dados'
path_destiny = r'C:\Users\vinic\python_projects\monitoracao_project\dados_parquet'

folders = listdir(path_sources)
# folders = [folders[0]] # teste com uma pasta só
# print(folders)

errors = [] # Guarda qualquer arquivo que falhou em ser carregado

for i in range(len(path_sources)):

    path_sour = path_sources+'\\'+folders[1]
    path_dest = path_destiny+'\\'+folders[1]

    mkdir(path_dest) # cria pastas de acordo com o nome da pasta de origem
    files = listdir(path_sour)

    multi_index = []

    for j in files:
        props = j.split('_')

        if 'accel' in path_sources[i]:
            multi_index.append([props[1], props[3], props[5], props[6]])

        elif 'gps' in path_sources[i]:
            multi_index.append([props[1], props[3], props[5], '1'])
            multi_index.append([props[1], props[3], props[5], '2'])
            multi_index.append([props[1], props[3], props[5], '3'])
            multi_index.append([props[1], props[3], props[5], '4'])
            multi_index.append([props[1], props[3], props[5], '5'])


    alldatas = pd.DataFrame(multi_index, columns=['value'],)

    for j in files:

        l = path_sour+'\\'+j
        m = path_dest+'\\'+j

        try:
            with h5py.File(l, 'r') as f:
                data = np.assaray(f.get('save_var')).T
                #data = pd.DataFrame(np.asarray(data).T)
                #datas[j]=data
                #data.to_csv(m[:-4]+'.csv', index=False, header=False)

                if 'accel' in path_sources[i]:
                    alldatas[props[1], props[3], props[5], props[6]] = data

                elif 'gps' in path_sources[i]:
                    alldatas[props[1], props[3], props[5], '1'] = data[:, 0]
                    alldatas[props[1], props[3], props[5], '2'] = data[:, 1]
                    alldatas[props[1], props[3], props[5], '3'] = data[:, 2]
                    alldatas[props[1], props[3], props[5], '4'] = data[:, 3]
                    alldatas[props[1], props[3], props[5], '5'] = data[:, 4]
        
        except:
            try:
                data = scipy.io.loadmat(l)
                data = np.assarray(data[list(data.keys())[-1]])
                # datas[j]=data
                #data.to_csv(m[:-4]+'.csv', index=False, header=False)

                if 'accel' in path_sources[i]:
                    alldatas[props[1], props[3], props[5], props[6]] = data

                elif 'gps' in path_sources[i]:
                    alldatas[props[1], props[3], props[5], '1'] = data[:, 0]
                    alldatas[props[1], props[3], props[5], '2'] = data[:, 1]
                    alldatas[props[1], props[3], props[5], '3'] = data[:, 2]
                    alldatas[props[1], props[3], props[5], '4'] = data[:, 3]
                    alldatas[props[1], props[3], props[5], '5'] = data[:, 4]
                
            except:
                errors.append(l)  

    alldatas.to_parquet(path_dest)


"""
for j in range(datas[list(datas.keys())[0]].shape[1]):
    for i in range(len(datas.keys())):
        plt.plot(datas[list(datas.keys())[i]][j])
    plt.suptitle(f'type:{folders[0]}; column:{j}')
    plt.show()




x = pd.DataFrame(index=['x', 'y'])
x['x','z']=np.array([2, 3, 5])
"""