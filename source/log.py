
import traceback

import sys
import os

allOff = True
cloudLog = True
logger = None
tid = 'tiddefault'


if not allOff and cloudLog:
  bucket = 'main'
  try:
    from google.cloud import logging
    logging_client = logging.Client('hosting-2718')
    logger = logging_client.logger(bucket)
  except:
    pass

def log(entry, bucket='main', severity='INFO'):
  if allOff:
    return
  try:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    entry += ' ' + str(exc_type)
    entry += ' ' + str(exc_obj)
    if not exc_type:
      pass
    else:
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      entry +=  ' '+str(fname)+' '+ str(exc_tb.tb_lineno)
      entry += ' ' + str(traceback.extract_tb(exc_tb))
      entry += ' ' + str(traceback.extract_stack())
  except Exception as e:
    entry += ' bad exc_info' + str(e)
  if logger:
    try:
      logger.log_text(str(entry) + tid, severity=severity)
    except Exception as e:
      print >> sys.stderr, 'failed logging', str(e)
  else:
    try:
      print >> sys.stderr, str(str(entry).encode('utf-8', 'replace'))
    except Exception as e:
      print >> sys.stderr, 'failed printing', str(e)

def debug(*entry):
  log(str(entry), 'main', 'DEBUG')

def info(*entry):
  log(str(entry), 'main', 'INFO')

def warn(*entry):
  log(str(entry), 'main', 'WARNING')

def error(*entry):
  log(str(entry), 'main', 'ERROR')
  
  

#logging_client = logging.Client()
#logger = logging_client.logger(bucket)
#logger.log_text(entry, severity=severity)
#print entry,bucket,severity
