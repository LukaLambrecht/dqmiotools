#!/usr/bin/env python

# Convert data from ROOT to parquet
# Looper over convert_data.py

# imports
import sys
import os
import argparse
sys.path.append(os.path.abspath('../jobsubmission'))
import condortools as ct


if __name__=='__main__':

  # read arguments
  parser = argparse.ArgumentParser(description='Convert data')
  parser.add_argument('-i', '--inputfiles', required=True, nargs='+')
  parser.add_argument('--runmode', default='local', choices=['local','condor'])
  parser.add_argument('--cmssw', default=None)
  args = parser.parse_args()

  # print arguments
  print('Running with following configuration:')
  for arg in vars(args):
    print('  - {}: {}'.format(arg,getattr(args,arg)))

  # loop over input files
  cmds = []
  for inputfile in args.inputfiles:
    cmd = 'python3 convert_data.py'
    cmd += ' -i {}'.format(inputfile)
    cmd += ' --runmode local'
    cmds.append(cmd)

  # run or submit commands
  if args.runmode=='condor':
    ct.submitCommandsAsCondorCluster('cjob_convert_data', cmds,
      cmssw_version=args.cmssw, home='auto')
  else:
    for cmd in cmds:
      print(cmd)
      os.system(cmd) 
