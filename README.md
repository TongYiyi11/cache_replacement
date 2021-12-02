<p align="center">
  <h1 align="center"> Cache Replacement Policy for LLC </h1>
  <p>
  A new cache replacement policy is proposed here based on the simulator
  used in Cache Replacement Championship (ChampSim: https://github.com/ChampSim/ChampSim.git).
  </p>

# 1. Instructions to Run the Simulator

**Compile**

ChampSim takes five parameters: Branch predictor, L1D prefetcher, L2C prefetcher, LLC replacement policy, and the number of cores. 
For example, `./build_champsim.sh bimodal no no lru 1` builds a single-core processor with bimodal branch predictor, no L1/L2 data prefetchers, and the baseline LRU replacement policy for the LLC.
```
$ ./build_champsim.sh bimodal no no no no lru 1

$ ./build_champsim.sh ${BRANCH} ${L1I_PREFETCHER} ${L1D_PREFETCHER} ${L2C_PREFETCHER} ${LLC_PREFETCHER} ${LLC_REPLACEMENT} ${NUM_CORE}
```

**Run simulation**

Execute `run_champsim.sh` with proper input arguments. The default `TRACE_DIR` in `run_champsim.sh` is set to `$PWD/crc2_traces`. <br>

* Single-core simulation: Run simulation with `run_champsim.sh` script.

```
Usage: ./run_champsim.sh [BINARY] [N_WARM] [N_SIM] [TRACE] [OPTION]
$ ./run_champsim.sh bimodal-no-no-no-no-lru-1core 1 10 400.perlbench-41B.champsimtrace.xz

${BINARY}: ChampSim binary compiled by "build_champsim.sh" (bimodal-no-no-lru-1core)
${N_WARM}: number of instructions for warmup (1 million)
${N_SIM}:  number of instructinos for detailed simulation (10 million)
${TRACE}: trace name (400.perlbench-41B.champsimtrace.xz)
${OPTION}: extra option for "-low_bandwidth" (src/main.cc)
```
Simulation results will be stored under "results_${N_SIM}M" as a form of "${TRACE}-${BINARY}-${OPTION}.txt".<br> 

* Multi-core simulation: Run simulation with `run_4core.sh` script. <br>
```
Usage: ./run_4core.sh [BINARY] [N_WARM] [N_SIM] [N_MIX] [TRACE0] [TRACE1] [TRACE2] [TRACE3] [OPTION]
$ ./run_4core.sh bimodal-no-no-no-lru-4core 1 10 0 400.perlbench-41B.champsimtrace.xz \\
  401.bzip2-38B.champsimtrace.xz 403.gcc-17B.champsimtrace.xz 410.bwaves-945B.champsimtrace.xz
```
Note that we need to specify multiple trace files for `run_4core.sh`. `N_MIX` is used to represent a unique ID for mixed multi-programmed workloads. 


# 2. Instructions to Run Our Replacement Policy
Our main algorithm is in the file ./replacement/myrepl.llc_repl.

**Compile**
<p>
Compare our policy with LRU and SHIP for single core configuration:
</p>

```
$ ./build_champsim.sh bimodal no no no no lru 1
$ ./build_champsim.sh bimodal no no no no ship 1
$ ./build_champsim.sh bimodal no no no no myrepl 1
```
<p>
  Compare our Policy with LRU and SHIP for quad core configuration:
</p>

```
$ ./build_champsim.sh bimodal no no no no lru 4
$ ./build_champsim.sh bimodal no no no no ship 4
$ ./build_champsim.sh bimodal no no no no myrepl 4
```
**Run**
<p>
  Run one trace under ./crc2_traces for single core and quad cores:
</p>

```
$ ./run_champsim.sh bimodal-no-no-no-no-lru-1core 1 10 soplex_205B.trace.xz
$ ./run_champsim.sh bimodal-no-no-no-no-lru-4core 4 10 0 bwaves_1609B.trace.xz bzip2_183B.trace.xz cactusADM_734B.trace.xz gamess_247B.trace.xz
$ ./run_champsim.sh bimodal-no-no-no-no-ship-1core 1 10 soplex_205B.trace.xz
$ ./run_champsim.sh bimodal-no-no-no-no-ship-4core 4 10 0 bwaves_1609B.trace.xz bzip2_183B.trace.xz cactusADM_734B.trace.xz gamess_247B.trace.xz
$ ./run_champsim.sh bimodal-no-no-no-no-myrepl-1core 1 10 soplex_205B.trace.xz
$ ./run_champsim.sh bimodal-no-no-no-no-myrepl-4core 4 10 0 bwaves_1609B.trace.xz bzip2_183B.trace.xz cactusADM_734B.trace.xz gamess_247B.trace.xz
```

<p>
  Run all the traces under ./crc2_traces for single core and quad cores:
</p>

```
$ ./batch_run.sh
$ ./batch_run_4core.sh
```

**Evaluation**
<p>
  Comparison of different policies:
</p>

```
$ python3 ./plot.py [dir] [multicore_flag] [outfile_path]
$ python3 plot.py ./results_10M/ 0 ./img/1core.png
$ python3 plot.py ./results_4core_10M/ 1 ./img/4cores.png
```
`dir` indicates the directory of the results after running the policies;
`multicore_flag` indicates single core (0) or quad cores (1);
`outfile_path` indicates the png file to be saved and external packages 
are required for saving multicore image (Please see https://altair-viz.github.io/user_guide/saving_charts.html).

<p>
  Sensitivity analysis of sample size:
</p>

```
./batch_sample.sh
```

# Authorization
All the source code can be found on https://github.com/TongYiyi11/cache_replacement.git.
If there's any problem, please contact yt2239@nyu.edu