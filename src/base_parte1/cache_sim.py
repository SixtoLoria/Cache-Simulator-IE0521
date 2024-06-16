from optparse import OptionParser
import gzip
from cache import *

import os


# Definir diferentes combinaciones de parámetros
cache_capacities = [8, 16, 32, 64, 128]
cache_assocs = [1, 2, 4, 8, 16]
block_sizes = [16, 32, 64, 128]
repl_policies = ['l', 'r']

# Carpeta que contiene los archivos .gz
trace_folder = 'traces/'
'''
parser = OptionParser()
parser.add_option("-s", dest="cache_capacity")
parser.add_option("-a", dest="cache_assoc")
parser.add_option("-b", dest="block_size")
parser.add_option("-r", dest="repl_policy")
parser.add_option("-t", dest="TRACE_FILE")

(options, args) = parser.parse_args()

cache = cache(options.cache_capacity, options.cache_assoc, options.block_size, options.repl_policy)
'''

"""
i = 0 #SOLO PARA DEBUG
with gzip.open(options.TRACE_FILE,'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        access_type, hex_str_address  = line.split(" ")
        address = int(hex_str_address, 16)
        cache.access(access_type, address)
        #SOLO PARA DEBUG
        #i+=1
        #if i == 25:
        #    break
cache.print_stats()
"""

#   Iterar sobre todos los archivos .gz en la carpeta especificada
for trace_file in os.listdir(trace_folder):
    if trace_file.endswith('.gz'):
        trace_path = os.path.join(trace_folder, trace_file)
        
        for capacity in cache_capacities:
            for assoc in cache_assocs:
                for block_size in block_sizes:
                    for policy in repl_policies:
                        # Inicializar la caché con los parámetros dados
                        cache_instance = cache(capacity, assoc, block_size, policy)
                        
                        # Leer el archivo de trazas y acceder a la caché
                        with gzip.open(trace_path, 'rt') as trace_fh:
                            for line in trace_fh:
                                line = line.rstrip()
                                access_type, hex_str_address = line.split(" ")
                                address = int(hex_str_address, 16)
                                cache_instance.access(access_type, address)
                        
                        # Capturar las estadísticas de la caché
                        print(f"Trace file: {trace_file}, Capacity: {capacity}kB, Assoc: {assoc}, Block size: {block_size}B, Policy: {policy}")
                        cache_instance.print_stats()
                        print("\n")