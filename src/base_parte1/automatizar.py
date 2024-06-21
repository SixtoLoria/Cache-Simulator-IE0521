from optparse import OptionParser
import gzip
from cache import *

import os


# Valores por defecto
default_capacity = 32
default_assoc = 8
default_block_size = 64
default_policy = 'l'

# Definir diferentes combinaciones de parámetros
cache_capacities = [8, 16, 32, 64, 128]
cache_assocs = [1, 2, 4, 8, 16]
block_sizes = [16, 32, 64, 128]
repl_policies = ['l', 'r']


# Carpeta que contiene los archivos .gz
trace_folder = 'traces/'

# Archivo de salida para los resultados
output_file = 'cache_simulation_results.txt'

def run_simulation(capacity, assoc, block_size, policy, trace_path):
    print(f"Running simulation with Capacity: {capacity}kB, Assoc: {assoc}, Block size: {block_size}B, Policy: {policy}")
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
    stats = cache_instance.print_stats()
    return stats

# Abrir el archivo de salida en modo escritura
with open(output_file, 'w') as out_fh:
    # Iterar sobre todos los archivos .gz en la carpeta especificada
    for trace_file in os.listdir(trace_folder):
        if trace_file.endswith('.gz'):
            trace_path = os.path.join(trace_folder, trace_file)
            print(f"Processing trace file: {trace_file}")

            # Variar capacidad
            for capacity in cache_capacities:
                print(f"  Varying cache capacity: {capacity}kB")
                stats = run_simulation(capacity, default_assoc, default_block_size, default_policy, trace_path)
                out_fh.write(f"Trace file: {trace_file}, Capacity: {capacity}kB, Assoc: {default_assoc}, Block size: {default_block_size}B, Policy: {default_policy}\n")
                out_fh.write(stats + "\n")
                out_fh.write("-" * 40 + "\n")
            
            # Variar asociatividad
            for assoc in cache_assocs:
                print(f"  Varying cache associativity: {assoc}")
                stats = run_simulation(default_capacity, assoc, default_block_size, default_policy, trace_path)
                out_fh.write(f"Trace file: {trace_file}, Capacity: {default_capacity}kB, Assoc: {assoc}, Block size: {default_block_size}B, Policy: {default_policy}\n")
                out_fh.write(stats + "\n")
                out_fh.write("-" * 40 + "\n")
            
            # Variar tamaño de bloque
            for block_size in block_sizes:
                print(f"  Varying block size: {block_size}B")
                stats = run_simulation(default_capacity, default_assoc, block_size, default_policy, trace_path)
                out_fh.write(f"Trace file: {trace_file}, Capacity: {default_capacity}kB, Assoc: {default_assoc}, Block size: {block_size}B, Policy: {default_policy}\n")
                out_fh.write(stats + "\n")
                out_fh.write("-" * 40 + "\n")
            
            # Variar política de reemplazo
            for policy in repl_policies:
                print(f"  Varying replacement policy: {policy}")
                stats = run_simulation(default_capacity, default_assoc, default_block_size, policy, trace_path)
                out_fh.write(f"Trace file: {trace_file}, Capacity: {default_capacity}kB, Assoc: {default_assoc}, Block size: {default_block_size}B, Policy: {policy}\n")
                out_fh.write(stats + "\n")
                out_fh.write("-" * 40 + "\n")

print("Simulations completed. Results saved in", output_file)