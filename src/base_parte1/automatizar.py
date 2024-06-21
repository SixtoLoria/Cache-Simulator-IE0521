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

# Archivo de salida para los resultados
output_file = 'cache_simulation_results.txt'

# Abrir el archivo de salida en modo escritura
with open(output_file, 'w') as out_fh:
    # Iterar sobre todos los archivos .gz en la carpeta especificada
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
                            out_fh.write(f"Trace file: {trace_file}, Capacity: {capacity}kB, Assoc: {assoc}, Block size: {block_size}B, Policy: {policy}\n")
                            out_fh.write(cache_instance.print_stats() + "\n")
                            out_fh.write("\n")