from sql import fetch
from sql import commit
import time
import sel as selenium
import gmail
import schema
import log
import hashlib
import datetime
import string
import random 
from datetime import timedelta

salt = 'mysalt'

def newHash():
  lets = string.ascii_letters[:26] + string.digits
  ans = 'tid'
  for i in range(8):
    ans += random.choice(lets)
  return ans
  
def hashEmail(email):
  email = email.lower() + salt
  m = hashlib.sha256()
  m.update(email)
  digest = m.hexdigest()
  return digest

class UnSub:
  def __init__(self, url, email, hashh):
    self.url = url
    self.email = email
    self.hashh = hashh
  def __repr__(self):
    return self.url + "  " + self.email

def refreshList():
  results = fetch('select url, email, hash from unsubs')
  l = list()
  for r in results:
    l.append(UnSub(r[0], r[1], r[2]))
  return l

def getFive():
  results = fetch('select url, email, hash from unsubs order by RAND() limit 5')
  s = set()
  for r in results:
    s.add(str(r[2]))
  origSet = s
  if not s:
    return []
  s = str(list(s)).replace('[','(').replace(']',')')
  results = fetch('select url, email, hash from unsubs where hash in ' + s)
  l = list()
  for r in results:
    l.append(UnSub(r[0], r[1], r[2]))
  return l, origSet
  
def anonymousAnalytics(email, unsubhash, success=False):
  digest = hashEmail(email)
  
  now = str(datetime.datetime.now())
  results = fetch('select unsubhash, success from anonymousanalytics where unsubhash=%s', (unsubhash))
  success = int(success)
  if results:
    if int(results[0][1]) == 0 and success:
      commit('update anonymousanalytics set success=1 where unsubhash=%s', (unsubhash))
    else:
      log.info('unsub hash is still failing, do not update analytics', unsubhash)
  else:
    commit('insert into anonymousanalytics (emailhash, unsubhash, success, stamp) values (%s, %s, %s, %s)', (digest, unsubhash, str(success), now))
  
def fullAnalytics(email, url, success):
  s = int(success)
  commit('insert into analytics (email, url, success) values (%s, %s, %s)', (email, url, s))
    
def addEmailToSqlAnalytics(uns, success=False):
  email = uns.email
  hashh = uns.hashh
  url = uns.url
  anonymousAnalytics(email, hashh, success)
  if url:
    fullAnalytics(email, url, success)
    
  
def deleteEntry(unsub, alll=False):
  if alll:
    commit('delete from unsubs where hash=%s',(unsub.hashh))
  else:
    commit('delete from unsubs where url=%s and email=%s',(unsub.url, unsub.email))
  
def handleDB(ll):
  ll, origSet = getFive()
  log.info(ll)
  if not ll:
    return
  browser,display = selenium.getBrowser()
  for uns in ll:
    log.info(uns)
    res = unsubscribe(uns, browser)
    if not res:
      log.info('failed confirmation', uns)
      addEmailToSqlAnalytics(uns,False)
    else:
      log.info('confirmed unsub')
      commit('insert into usercount (another) values (1)')
      addEmailToSqlAnalytics(uns,True)
    browser,display = selenium.refreshBrowser(browser,display)
  for ss in origSet:
    commit('delete from unsubs where hash=%s', ss)
  browser.quit()

def unsubscribe(unsub, browser):
  try:
    a = selenium.processPage(unsub,browser)
    return a
  except Exception as e:
    log.info(e)
  return False
  
def mainMaster(wipe=False):
  log.tid = newHash()
  if wipe:
    schema.wipe()
  mail =  gmail.connect()
  log.info('print analytics total, successful, all broken')
  results = fetch('select count(*) from analytics')
  log.info('total', results)
  results = fetch('select count(*) from analytics where success=1')
  log.info('successful', results)
  results = fetch('select email, url from analytics where success=0')
  log.info(results)

  rr = random.randint(20,21)
  time.sleep(rr)
  it = 0
  while True:
    it += 1
    log.info('reading email')
    uss = None
    try:
      uss = gmail.readEmailFromGmail(mail)
    except Exception as e:
      log.info('exception', e)
      if it % 2 == 0:
        mail = gmail.connect()
    sleeplen = 3600
    log.info('sleeping for '+str(sleeplen))
    if it % 1000 == 0:
      mail = gmail.connect()
    time.sleep(sleeplen)

def getAnalyticsForEmail(email):
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

def printAnalytics():
  log.tid = newHash()
  results = fetch('select * from analytics')
  log.info('all analytics', results)
  results = fetch('select count(*) from unsubs')
  log.info('current unsubs', results)
  log.info('print analytics total, successful, all broken')
  results = fetch('select count(*) from analytics')
  log.info('total', results)
  results = fetch('select count(*) from analytics where success=1')
  log.info('successful', results)
  results = fetch('select email, url from analytics where success=0')
  log.info(results)
  log.info('success / not success for william.k.dvorak')
  log.info(getAnalyticsForEmail('william.k.dvorak@gmail.com'))
    
def mainSlave():
  log.tid = newHash()
  log.info('print analytics total, successful, all broken')
  results = fetch('select count(*) from analytics')
  log.info('total', results)
  results = fetch('select count(*) from analytics where success=1')
  log.info('successful', results)
  results = fetch('select email, url from analytics where success=0')
  log.info(results)
  rr = random.randint(20,40)
  time.sleep(rr)
  it = 0
  while True:
    it += 1
    uss = None
    log.info('handling unsubs')
    results = fetch('select * from unsubs')
    log.info(results)
    results = fetch('select * from readmail')
    log.info(results)
    try:
      handleDB(uss)
    except Exception as e:
      log.info('exception', e)
    sleeplen = 20
    log.info('sleeping for '+str(sleeplen))
    time.sleep(sleeplen)
    