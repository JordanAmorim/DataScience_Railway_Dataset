# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from os import listdir
from os.path import isfile, join
import shutil

#-----------------------------------------------------------------------------------------
#GPS files naming rules
#-----------------------------------------------------------------------------------------

#{file#}_{date}_{root index}_{daily passing#}_{region#}_{running direction}.mat

#running direction: 1 - outbound,  2 - inbound

#-----------------------------------------------------------------------------------------
#Acceleration files naming rules
#-----------------------------------------------------------------------------------------

#{file#}_{date}_{root index}_{daily passing#}_{region#}_{running direction}_{sensor channel}.mat

#running direction: 1 - outbound, 2 - inbound

# ----------------------------- #
# LRV4306: acceleration data

# pasta de origem
LRV4306_accel = 'G:\\.shortcut-targets-by-id\\1oKn7IN7zznQuhwjDCDdjq8r9wHJYBEhj\\DR_Train\\LRV4306\\accelerometer_data'
onlyfiles = [f for f in listdir(LRV4306_accel) if isfile(join(LRV4306_accel, f))]

regiao = '5'

# Pasta de destino
dst_path = 'C:\\Users\\vinic\\python_projects\\monitoracao_project\\dados\\LRV4306_accelerometer_data'
n = 0
lg = len(onlyfiles)
for i in onlyfiles:
    under = 0
    posic = 0
    for j in range(len(i)):
        if i[j] == '_' and under <= 3:
            under += 1
            posic = j+1
    
    if i[posic] == regiao:
        src_path = LRV4306_accel+'\\'+i
        shutil.copy(src_path, dst_path)
        n += 1
        print(f'{n}/{lg}')

#----------------------------------------------
# LRV4306: gps data

LRV4306_gps = 'G:\\.shortcut-targets-by-id\\1oKn7IN7zznQuhwjDCDdjq8r9wHJYBEhj\\DR_Train\\LRV4306\\gps_data'
onlyfiles = [f for f in listdir(LRV4306_gps) if isfile(join(LRV4306_gps, f))]

regiao = '5'

dst_path = 'C:\\Users\\vinic\\python_projects\\monitoracao_project\\dados\\LRV4306_gps_data'
n = 0
lg = len(onlyfiles)
for i in onlyfiles:
    under = 0
    posic = 0
    for j in range(len(i)):
        if i[j] == '_' and under <= 3:
            under += 1
            posic = j+1
    
    if i[posic] == regiao:
        src_path = LRV4306_gps+'\\'+i
        shutil.copy(src_path, dst_path)
        n += 1
        print(f'{n}/{lg}')

# ----------------------------- #
# LRVLRV4313: acceleration data

LRV4313_accel = 'G:\\.shortcut-targets-by-id\\1oKn7IN7zznQuhwjDCDdjq8r9wHJYBEhj\\DR_Train\\LRV4313\\accelerometer_data'
onlyfiles = [f for f in listdir(LRV4313_accel) if isfile(join(LRV4313_accel, f))]

regiao = '5'

dst_path = 'C:\\Users\\vinic\\python_projects\\monitoracao_project\\dados\\LRV4313_accelerometer_data'
n = 0
lg = len(onlyfiles)
for i in onlyfiles:
    under = 0
    posic = 0
    for j in range(len(i)):
        if i[j] == '_' and under <= 3:
            under += 1
            posic = j+1
    
    if i[posic] == regiao:
        src_path = LRV4313_accel+'\\'+i
        shutil.copy(src_path, dst_path)
        n += 1
        print(f'{n}/{lg}')


#----------------------------------------------
# LRV4306: gps data

LRV4313_gps = 'G:\\.shortcut-targets-by-id\\1oKn7IN7zznQuhwjDCDdjq8r9wHJYBEhj\\DR_Train\\LRV4313\\gps_data'
onlyfiles = [f for f in listdir(LRV4313_gps) if isfile(join(LRV4313_gps, f))]

regiao = '5'

dst_path = 'C:\\Users\\vinic\\python_projects\\monitoracao_project\\dados\\LRV4313_gps_data'
n = 0
lg = len(onlyfiles)
for i in onlyfiles:
    under = 0
    posic = 0
    for j in range(len(i)):
        if i[j] == '_' and under <= 3:
            under += 1
            posic = j+1
    
    if i[posic] == regiao:
        src_path = LRV4313_gps+'\\'+i
        shutil.copy(src_path, dst_path)
        n += 1
        print(f'{n}/{lg}')