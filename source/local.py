import datetime
from datetime import timedelta
import os

def hashEmail(a):
  return 'aoeu'

import sql
from sql import fetch


#import sel

class Uns:
  pass
  
def doUns():
  from selenium import webdriver
  from selenium.webdriver.common.keys import Keys
  print '1'
  driver = webdriver.Firefox()
  print '2'
  driver.get("http://www.python.org")
  print '3'
  assert "Python" in driver.title
  print '4'
  return
  import time
  uns = Uns()
  uns.url='https://click.message.fedex.com/?qs=a2d39ce5274aae028bee17e957371943e3fd281bf03dd1f0a3d9f21d7485636a7c3adb30cca5f54411b2950e842dfe89047581c60e19e136'
  uns.email='william.k.dvorak@gmail.com'
  uns.hashh = 'default'
  browser = sel.getBrowserNoDisplay()
  print 'hre22',browser
  print sel.processPage(uns,browser)
  time.sleep(30)
  browser = sel.getBrowser()
  print 'hre',browser
  print sel.processPage(uns,browser)
  browser = sel.getBrowserNoDisplay()
  print 'hre22',browser
  print sel.processPage(uns,browser)
  print 'done'


def allUnsuccessful():
  results = fetch('select email, url from analytics where success=0')
  ss = dict()
  for r in results:
    ss[str(r[1])] = str(r[0])
  i = 0
  low = 200
  high = low+10
  print len(ss.keys())
  for k,v in ss.iteritems():
    if i > low:
      os.system('open '+k)
      print v
      print k
    i+=1
    if i > high:
      break
    
allUnsuccessful()

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