from google.cloud import logging

import sys

cloudLog = True
logger = None


if cloudLog:
  bucket = 'main'
  try:
    logging_client = logging.Client('consulting-2718')
    logger = logging_client.logger(bucket)
  except:
    pass

def log(entry, bucket='main', severity='INFO'):
  if logger:
    try:
      logger.log_text(str(entry), severity=severity)
    except Exception as e:
      print >> sys.stderr, 'failed logging', str(e)
  else:
    try:
      print >> sys.stderr, str(str(entry).encode('utf-8', 'replace'))
    except Exception as e:
      print >> sys.stderr, 'failed printing', str(e)

def debug(entry, bucket='main'):
  log(entry, bucket, 'DEBUG')

def info(entry, bucket='main'):
  log(entry, bucket, 'INFO')

def warn(entry, bucket='main'):
  log(entry, bucket, 'WARNING')

def error(entry, bucket='main'):
  log(entry, bucket, 'ERROR')
  

#logging_client = logging.Client()
#logger = logging_client.logger(bucket)
#logger.log_text(entry, severity=severity)
#print entry,bucket,severity
