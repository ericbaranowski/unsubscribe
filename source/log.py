from google.cloud import logging

import sys

cloudLog = True
logger = None
tid = 'tiddefault'


if cloudLog:
  bucket = 'main'
  try:
    logging_client = logging.Client('hosting-2718')
    logger = logging_client.logger(bucket)
  except:
    pass

def log(entry, bucket='main', severity='INFO'):
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
