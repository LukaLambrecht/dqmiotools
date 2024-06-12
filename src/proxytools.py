######################################
# Collection of proxy handling tools #
######################################


import sys
import os


def export_proxy( proxy ):
  ### export a provided proxy to the system variables
  print('exporting proxy to {}'.format(proxy))
  os.environ["X509_USER_PROXY"] = proxy
