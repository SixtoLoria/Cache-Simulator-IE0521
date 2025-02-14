from optparse import OptionParser
import gzip
import sys
from cache import *

parser = OptionParser()
parser.add_option("--l1_s", dest="l1_s")
parser.add_option("--l1_a", dest="l1_a")
parser.add_option("--l2", action="store_true", dest="has_l2")
parser.add_option("--l2_s", dest="l2_s")
parser.add_option("--l2_a", dest="l2_a")
parser.add_option("--l3", action="store_true", dest="has_l3")
parser.add_option("--l3_s", dest="l3_s")
parser.add_option("--l3_a", dest="l3_a")
parser.add_option("-b", dest="block_size", default="64")
parser.add_option("-r", dest="repl_policy")
parser.add_option("-t", dest="TRACE_FILE")
parser.add_option("--csv", action="store_true", dest="csv") # opción para desplegar resultados en formato csv

(options, args) = parser.parse_args()

# manejo de errores
if options.TRACE_FILE == None:
    print("ERROR: trace no proporcionado")
    sys.exit()

if options.l1_s == None or options.l1_a == None:
    print("ERROR: debe especificar los parámetros del caché L1")
    sys.exit()
if (options.l2_s == None or options.l2_a == None) and options.has_l2 != None:
    print("ERROR: debe especificar los parámetros del caché L2")
    sys.exit()
if (options.l3_s == None or options.l3_a == None) and options.has_l3 != None:
    print("ERROR: debe especificar los parámetros del caché L3")
    sys.exit()

if options.has_l2 == None and (options.l2_s != None or options.l2_a != None):
    print("ERROR: debe utilizar la bandera --l2")
    sys.exit()

if options.has_l3 == None and (options.l3_s != None or options.l3_a != None):
    print("ERROR: debe utilizar la bandera --l3")
    sys.exit()


# instanciar cachés
l1_cache = cache(options.l1_s, options.l1_a, options.block_size, 'l')

if options.has_l2:
    l2_cache = cache(options.l2_s, options.l2_a, options.block_size, 'l')

if options.has_l3:
    l3_cache = cache(options.l3_s, options.l3_a, options.block_size, 'l')

with gzip.open(options.TRACE_FILE,'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        access_type, hex_str_address  = line.split(" ")
        address = int(hex_str_address, 16)

        is_l1_miss = False
        is_l2_miss = False
        is_l3_miss = False

        is_l1_miss = l1_cache.access(access_type, address)

        if is_l1_miss and options.has_l2:
            is_l2_miss = l2_cache.access(access_type, address)
        
        if is_l2_miss and options.has_l3:
            _ = l3_cache.access(access_type, address)



if options.csv:
    result = l1_cache.get_stats_csv()

    if options.has_l2:
        result = f'{result},{l2_cache.get_stats_csv()}'

    if options.has_l3:
        result = f'{result},{l3_cache.get_stats_csv()}'
    
    print(result)

else:
    l1_cache.print_stats()

    if options.has_l2:
        l2_cache.print_stats()

    if options.has_l3:
        l3_cache.print_stats()