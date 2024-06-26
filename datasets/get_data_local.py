#!/usr/bin/env python3

# Get data from local storage
# Note: this is for the folder structure of T2_IIHE_BE,
#       will need modifications on other local storage sites.

# imports
import sys
import os
import json
import numpy as np
import argparse
import ROOT
# local imports (python3 version)
sys.path.append(os.path.abspath('../'))
from src.DQMIOReader import DQMIOReader
import jobsubmission.condortools as ct
PYTHON_EXE = 'python3'
# local imports (python2 version)
#sys.path.append(os.path.abspath('../src'))
#from DQMIOReader import DQMIOReader
#sys.path.append(os.path.abspath('../jobsubmission'))
#import condortools as ct
#PYTHON_EXE = 'python'


def get_all_root_files(directory):
    # get all root files in all subdirectories of directory
    rootfiles = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.root'): rootfiles.append(os.path.join(root,f))
    return rootfiles

def format_dataset_name(dataset):
    # format the name of a local dataset (i.e. a local folder)
    # into a more convenient naming for the output file,
    # also consistent with get_data (remote data reading).
    dataset = dataset.strip('/')
    parts = dataset.split('/')
    processing_tag = parts[-1]
    tier = parts[-2]
    primary_dataset = parts[-3]
    era = parts[-4]
    newname = '-'.join([primary_dataset, era, processing_tag, tier])
    return newname


if __name__=='__main__':

  # read arguments
  parser = argparse.ArgumentParser(description='Get data')
  parser.add_argument('-d', '--datasetname', required=True)
  parser.add_argument('-m', '--menames', required=True)
  parser.add_argument('-o', '--outputdir', default='.')
  parser.add_argument('--runmode', default='local', choices=['local', 'condor'])
  parser.add_argument('--cmssw', default=None)
  parser.add_argument('--test', default=False, action='store_true')
  args = parser.parse_args()
  
  # print arguments
  print('Running with following configuration:')
  for arg in vars(args):
    print('  - {}: {}'.format(arg,getattr(args,arg)))

  # handle job submission if requested
  if args.runmode=='condor':
    cmd = PYTHON_EXE + ' get_data_local.py'
    cmd += ' -d {}'.format(args.datasetname)
    cmd += ' -m {}'.format(args.menames)
    cmd += ' -o {}'.format(args.outputdir)
    if args.test: cmd += ' --test'
    cmd += ' --runmode local'
    ct.submitCommandAsCondorJob('cjob_get_data', cmd,
      cmssw_version=args.cmssw, home='auto')
    sys.exit()

  # print starting tag (for job completion checking)
  sys.stderr.write('###starting###\n')
  sys.stderr.flush()

  # make a list of input files
  inputfiles = get_all_root_files(args.datasetname)
  print('Found {} files for dataset {}'.format(len(inputfiles),args.datasetname))
  if args.test:
    print('WARNING: running in test mode, will processo only one file.')
    inputfiles = [inputfiles[0]]

  # make a list of monitoring elements
  menames = []
  with open(args.menames, 'r') as f:
    menames = json.load(f)

  # print configuration parameters
  print('Running with following parameters:')
  print('Input files ({}):'.format(len(inputfiles)))
  for inputfile in inputfiles: print('  - {}'.format(inputfile))
  print('Monitoring elements: ({})'.format(len(menames)))
  for mename in menames: print('  - {}'.format(mename))

  # make a DQMIOReader instance and initialize it with the DAS files
  print('Initializing DQMIOReader...')
  sys.stdout.flush()
  sys.stderr.flush()
  reader = DQMIOReader(*inputfiles, sortindex=True, nthreads=1)
  print('Initialized DQMIOReader with following properties')
  print('Number of lumisections: {}'.format(len(reader.listLumis())))
  print('Number of monitoring elements per lumisection: {}'.format(len(reader.listMEs())))

  # loop over monitoring elements
  for mename in menames:

    # select the monitoring element
    print('Selecting monitoring element {}...'.format(mename))
    mes = reader.getSingleMEs(mename)

    # sort the lumisections
    print('Sorting lumisections...')
    runs = np.array([me.run for me in mes]).astype(int)
    lumis = np.array([me.lumi for me in mes]).astype(int)
    ids = (runs*10000 + lumis).astype(int)
    sorted_inds = np.argsort(ids)

    # write selected monitoring elements to output file
    print('Writing output file...')
    if not os.path.exists(args.outputdir): os.makedirs(args.outputdir)
    outputfile = (format_dataset_name(args.datasetname)+'-'+mename).strip('/').replace('/','-')+'.root'
    outputfile = os.path.join(args.outputdir, outputfile)
    f = ROOT.TFile.Open(outputfile, 'recreate')
    for idx in sorted_inds:
      me = mes[idx]
      name = 'run{}_ls{}_{}'.format(me.run, me.lumi, me.name.replace('/','_'))
      me.data.SetName(name)
      me.data.SetTitle(name)
      me.data.Write()
    f.Close()

  # print finishing tag (for job completion checking)
  sys.stderr.write('###done###\n')
  sys.stderr.flush()
