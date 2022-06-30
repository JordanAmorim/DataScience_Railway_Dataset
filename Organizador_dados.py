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
#from gettext import install


import h5py
import numpy as np
import scipy.io
from os import listdir
from os import mkdir
import pandas as pd
#import matplotlib.pyplot as plt

"""Pasta de origem dos dados e pasta de destino para os dados trabalhados"""
path_sources = r'C:\Users\vinic\python_projects\monitoracao_project\dados'
path_destiny = r'C:\Users\vinic\python_projects\monitoracao_project\dados_parquet'

folders = listdir(path_sources)
# print(folders)

errors = [] # Guarda qualquer arquivo que falhou em ser carregado

acel_props = 'date_root index_daily passing_region_running direction_sensor channel'.split('_')
gps_props = 'date_root index_daily passing_region_running direction'.split('_')

for i in range(len(path_sources)):

    path_sour = path_sources+'\\'+folders[1]
    path_dest = path_destiny+'\\'+folders[1]

    mkdir(path_dest) # cria pastas de acordo com o nome da pasta de origem
    files = listdir(path_sour)

    if 'acel' in path_sources[i]:
        datas = pd.DataFrame(acel_props)

    elif 'gps' in path_sources[i]:
        datas = pd.DataFrame(gps_props)

    for j in files:

        l = path_sour+'\\'+j
        m = path_dest+'\\'+j

        

        try:
            with h5py.File(l, 'r') as f:
                data = f.get('save_var')
                data = pd.DataFrame(np.asarray(data).T)
                datas[j]=data
                #data.to_csv(m[:-4]+'.csv', index=False, header=False)
        except:
            try:
                data = scipy.io.loadmat(l)
                data = pd.DataFrame(data[list(data.keys())[-1]])
                datas[j]=data
                #data.to_csv(m[:-4]+'.csv', index=False, header=False)
                
            except:
                errors.append(l)   


for j in range(datas[list(datas.keys())[0]].shape[1]):
    for i in range(len(datas.keys())):
        plt.plot(datas[list(datas.keys())[i]][j])
    plt.suptitle(f'type:{folders[0]}; column:{j}')
    plt.show()