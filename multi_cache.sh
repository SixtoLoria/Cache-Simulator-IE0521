trace_dir=`ls ./traces`

output=results/multi_cache_result.csv

# limpia el archivo
> $output

if [ $# -eq 0 ] || [ $1 == '1' ]; then
  for trace in $trace_dir; do
    trace_trim=`grep -io "^[0-9]*.[a-z0-9]*" <<< ${trace}`

    echo -n "L1,32,8,${trace_trim}," >> $output
    python3 ./src/base_parte2/cache_sim.py --l1_s 32 --l1_a 8 -t "traces/$trace" --csv >> $output
  done
fi


if [ $# -eq 0 ] || [ $1 == '2' ]; then
  for l2_s in 64 128; do
    for l2_a in 8 16; do
      for trace in $trace_dir; do
        trace_trim=`grep -io "^[0-9]*.[a-z0-9]*" <<< ${trace}`

        echo -n "L1+L2,${l2_s},${l2_a},${trace_trim}," >> $output
        python3 ./src/base_parte2/cache_sim.py --l1_s 32 --l1_a 8 --l2 --l2_s $l2_s --l2_a $l2_a -t "traces/$trace" --csv >> $output
      done
    done
  done
fi

if [ $# -eq 0 ] || [ $1 == '3' ]; then
  for l3_s in 512 1024; do
    for l3_a in 16 32; do
      for trace in $trace_dir; do
        trace_trim=`grep -io "^[0-9]*.[a-z0-9]*" <<< ${trace}`

        echo -n "L1+L2+L3,${l3_s},${l3_a},${trace_trim}," >> $output
        python3 ./src/base_parte2/cache_sim.py --l1_s 32 --l1_a 8 --l2 --l2_s 256 --l2_a 8 --l3 --l3_s $l3_s --l3_a $l3_a -t "traces/$trace" --csv >> $output
      done
    done
  done
fi