from google.cloud import logging

import sys

cloudLog = True


if cloudLog:
  logging_client = logging.Client('consulting-2718')
  logger = logging_client.logger(bucket)


def log(*entry):
  e = entry
  try:
    e = str(entry)
  except:
    e = entry
  try:
    if cloudLog:
      logger.log_text(e)
    print >> sys.stderr, str(e.decode('utf-8', 'replace'))
  except Exception as e:
    print e

def debug(entry, bucket='main'):
  return
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