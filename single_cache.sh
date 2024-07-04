trace_dir=`ls ./traces`

output=results/single_cache_result.csv

# limpia el archivo
> $output

# variar tamaño del cache
if [ $# -eq 0 ] || [ $1 == 's' ]; then
	for cache_size in 8 16 32 64 128; do
		for trace in $trace_dir; do
			trace_trim=`grep -io "^[0-9]*.[a-z0-9]*" <<< ${trace}`

			echo -n "size,${cache_size},8,64,l,${trace_trim}," >> $output
			python3 ./src/base_parte1/cache_sim.py -s $cache_size -a 8 -b 64 -r l -t "./traces/$trace" --csv >> $output
		done
	done
fi

# variar associatividad
if [ $# -eq 0 ] || [ $1 == 'a' ]; then
	for way in 1 2 4 8 16; do
		for trace in $trace_dir; do
			trace_trim=`grep -io "^[0-9]*.[a-z0-9]*" <<< ${trace}`

			echo -n "way,32,${way},64,l,${trace_trim}," >> $output
			python3 ./src/base_parte1/cache_sim.py -s 32 -a $way -b 64 -r l -t "./traces/$trace" --csv >> $output
		done
	done
fi

# variar tamaño del bloque
if [ $# -eq 0 ] || [ $1 == 'b' ]; then
	for block in 16 32 64 128; do
		for trace in $trace_dir; do
			trace_trim=`grep -io "^[0-9]*.[a-z0-9]*" <<< ${trace}`

			echo -n "block,32,8,${block},l,${trace_trim}," >> $output
			python3 ./src/base_parte1/cache_sim.py -s 32 -a 8 -b $block -r l -t "./traces/$trace" --csv >> $output
		done
	done
fi

# variar política de reemplazo
if [ $# -eq 0 ] || [ $1 == 'p' ]; then
	for policy in l r; do
		for trace in $trace_dir; do
			trace_trim=`grep -io "^[0-9]*.[a-z0-9]*" <<< ${trace}`

			echo -n "policy,32,8,64,${policy},${trace_trim}," >> $output
			python3 ./src/base_parte1/cache_sim.py -s 32 -a 8 -b 64 -r $policy -t "./traces/$trace" --csv >> $output
		done
	done
fi