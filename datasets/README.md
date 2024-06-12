# Collect input data from DQMIO datasets

Read datasets from DAS and extract MEs of interest.

### Deprecation warning
These tools extract MEs directly from the DQMIO datasets.
While this works in principle, it is no longer the recommended approach,
as instead we now have the [DIALS](https://github.com/cms-DQM/dials-py) for this purpose.
You can use for example [these tools](https://github.com/LukaLambrecht/dialstools/tree/main/datasets),
which have a completely equivalent functionality as the ones here,
but using DIALS as interface instead of operating on the raw DQMIO datasets directly.

### Step 1: rucio request to get datasets locally (optional)
The original idea was to read the DQMIO datasets remotely and extract the data directly.
However, the datasets seem to be not or very instably available via DAS.

Therefore, the new approach is to request a temporary copy of the datasets on T2B via rucio.
See https://t2bwiki.iihe.ac.be/Rucio (or equivalent instructions for your local T2).
From there, the relevant data can be extracted and stored locally.

An alternative approach is to directly copy the datasets to a local location using [this tool](https://github.com/LukaLambrecht/dqmiotools/blob/master/copydas/copy_das_to_local_set.py) and run the remaining steps on the local copies as well.
After the relevent MEs have been extracted, the downloaded DQMIO datasets can be removed again to save disk space.

### Step 2: read DQMIO files and store MEs of interest in plain ROOT files
See `get_data.py` (for remote reading), `get_data_local.py` (for local reading) and `get_data_loop.py` (for looping over multiple datasets and/or MEs).

#### Random ROOT errors and CMSSW versions
The reading of DQMIO files and conversion of MEs into plain ROOT files for local storage
seems to give non-deterministic quasi-random errors when run with CMSSW 12.4.6 and python3,
while it runs fine with CMSSW 10.6.29 and python2, probably because of ROOT...
This also depends on the CMSSW version with which the DQMIO datasets were produced.
Also seems to give non-deterministic errors when run in multithreaded mode in jobs,
instead run with one thread.
Yet to be figured out why exactly, but it works for now...

### Step 3: conversion to parquet files
See `convert_data.py` and `convert_data_loop.py`

#### Overwriting warning
Note: parquet files apparently are not automatically overwritten,
instead the script fails and raises an error upon writing attempt,
so need to manually remove parquet files before re-running.

### Epilogue: check available lumisections
After the previous steps, you can check the lumisections present in the resulting `parquet` files
and compare to the lumisections in the DQMIO datasets on DAS,
as a check that all data was processed correctly.
See `check_lumis.py`.
