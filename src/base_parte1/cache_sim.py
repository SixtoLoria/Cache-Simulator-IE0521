from optparse import OptionParser
import gzip
from cache import *

parser = OptionParser()
parser.add_option("-s", dest="cache_capacity")
parser.add_option("-a", dest="cache_assoc")
parser.add_option("-b", dest="block_size")
parser.add_option("-r", dest="repl_policy")
parser.add_option("-t", dest="TRACE_FILE")
parser.add_option("--csv", action="store_true", dest="csv") # opción para desplegar resultados en formato csv

(options, args) = parser.parse_args()

cache = cache(options.cache_capacity.strip(), options.cache_assoc.strip(), options.block_size.strip(), options.repl_policy.strip())

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

if options.csv:
    cache.print_stats_csv()
else:
    cache.print_stats()
