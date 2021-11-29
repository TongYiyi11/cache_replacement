#!/bin/bash

for size in 64 128 256 512 1024
do
  sed -i.bak 's/SAMPLER_SET 256\*NUM_CPUS/SAMPLER_SET '${size}'\*NUM_CPUS/g' replacement/myrepl.llc_repl
  ./build_champsim.sh bimodal no no no no myrepl 1
  ./run_champsim_sample.sh bimodal-no-no-no-no-myrepl-1core 1 10 soplex_205B.trace.xz ${size}
  # Restore to the default configuration
  sed -i.bak 's/SAMPLER_SET '${size}'\*NUM_CPUS/SAMPLER_SET 256\*NUM_CPUS/g' replacement/myrepl.llc_repl
done