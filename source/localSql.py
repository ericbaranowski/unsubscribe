import datetime
from datetime import timedelta
def hashEmail(a):
  return 'aoeu'

import sql
from sql import fetch


def anal(email):
  digest = hashEmail(email)
  results = fetch('select count(*) from anonymousanalytics where emailhash=%s', digest)
  total = results[0][0]
  results = fetch('select count(*) from anonymousanalytics where emailhash=%s and success=1', digest)
  successful = results[0][0]
  if email == 'admin':
    results = fetch('select count(*) from anonymousanalytics')
    total = results[0][0]
    results = fetch('select count(*) from anonymousanalytics where success=1')
    successful = results[0][0]
  if email == 'admin24':
    now = str(datetime.datetime.now()-timedelta(hours=24))
    results = fetch('select count(*) from anonymousanalytics where stamp > %s', now)
    total = results[0][0]
    results = fetch('select count(*) from anonymousanalytics where success=1 and stamp > %s', now)
    successful = results[0][0]
  return [str(int(successful)), str(int(total)-int(successful))]