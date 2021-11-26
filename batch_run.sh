#!/bin/bash

for file in crc2_traces/*.xz;do
    filename=$(basename $file)
    echo "run traces: $filename"
#    ./run_champsim.sh bimodal-no-no-no-no-lru-1core 1 10 $filename
#    ./run_champsim.sh bimodal-no-no-no-no-ship-1core 1 10 $filename
    ./run_champsim.sh bimodal-no-no-no-no-myrepl-1core 1 10 $filename
  done