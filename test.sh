search_dir=`ls ./traces`

> results/test.txt

for entry in $search_dir
do
  python3 ./src/base_parte1/cache_sim.py -s 128 -a 16 -b 64 -r l -t "./traces/$entry" >> results/test.txt
done
