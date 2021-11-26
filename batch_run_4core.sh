#!/bin/bash

filearr=()
for file in crc2_traces/*.xz;
do
    filename=$(basename $file)
    filearr=("${filearr[@]}" $filename)
done

len=${#filearr[@]}
mix=0
for (( i=0; i<${len}; i+=4));
do
  echo "run traces: ${filearr[$i]} ${filearr[$i+1]} ${filearr[$i+2]} ${filearr[$i+3]}"
  ./run_4core.sh bimodal-no-no-no-no-lru-4core 1 10 $mix ${filearr[$i]} ${filearr[$i+1]} ${filearr[$i+2]} ${filearr[$i+3]}
  ./run_4core.sh bimodal-no-no-no-no-ship-4core 1 10 $mix ${filearr[$i]} ${filearr[$i+1]} ${filearr[$i+2]} ${filearr[$i+3]}
  ./run_4core.sh bimodal-no-no-no-no-myrepl-4core 1 10 $mix ${filearr[$i]} ${filearr[$i+1]} ${filearr[$i+2]} ${filearr[$i+3]}
  ((++mix))
done