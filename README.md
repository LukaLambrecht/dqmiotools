# Tools for producing and reading (per-lumisection) DQMIO files

### Introduction
This repository contains a collection of tools for producing and reading per-lumisection DQMIO files.
The production aspect is mainly focused on relatively small tests on a few lumisections, e.g. to test changes in the per-LS configuration for DQMIO.
The reading aspect consists of quick utility scripts, e.g. to find out which lumisections or monitoring elements (MEs) are available in a DQMIO file, as well as more involved harvesting scripts to read entire DQMIO datasets and extract particular MEs to be stored in a more convenient format.

### The per-lumisection DQMIO file format
More information about this file format can be found on [this twiki page](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PerLsDQMIO).

### Quick guide
The different tools in this repository are grouped in folders as follows:
- `commissioning`: check available lumisections and size of DQMIO datasets (mostly intended for internal usage with the 2022 nanoDQMIO re-reco campaign).
- `copydas`: copy single files or entire datasets from DAS to a local location (useful for not too large datasets when remote reading proves to be unstable).
- `harvesting`: read DQMIO files or datasets and extract MEs to a more convenient format.
- `jobsubmission`: tools for HTCondor job submission used throughout this repository.
- `production`: test changes in the per-lumisection DQMIO configuration.
- `reading`: utility scripts for quick DQMIO file diagnostics (e.g. which MEs, which lumisections, etc.)
- `src`: actual DQMIO reader class and other tools used throughout this repository.

### Loosely connected tips and tricks
#### Things to keep in mind when trying to read files from DAS:  
- You will need a valid grid certificate. Create one using `voms-proxy-init --voms cms`.
- The scripts in this repository should contain the correct export command. If you still get an error concerning X509\_USER\_PROXY, you can run the command `export X509_USER_PROXY=path` (where `path` should be replaced by the path to where you stored the proxy created in the previous step) and try again.

#### Special instructions for job submission:  
- You will need a valid grid certificate if accessing remote files via DAS (see above). Copy the proxy to a location that is accessible from the cluster nodes (e.g. somewhere in you home folder) and make sure to pass the path to it as the `proxy` argument to the job submission script.  
- You might also need to set a CMSSW environment, depending on the configuration of your cluster. At least on lxplus this appears to be needed. You can do this using the `cmssw` argument to the job submission script.
