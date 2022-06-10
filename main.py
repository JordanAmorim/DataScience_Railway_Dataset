'''
Script criado para exeplificar como carregar um arquivo .mat no Pythonzin.

By Will
'''


import numpy
import h5py


path = '<DIGITE_O_DIRETÓRIO_DO_ARQUIVO_AQUI>'

with h5py.File(path, 'r') as f:
    data = f.get('save_var')
    data = numpy.array(data)
