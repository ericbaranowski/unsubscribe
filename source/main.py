from sql import fetch
from sql import commit
import time
import sel as selenium
import gmail
import schema
import log
import hashlib
import datetime

def hashEmail(email):
  email = email.lower()
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
  results = fetch('select url, email, hash from unsubs limit 5')
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
  for ss in origSet:
    commit('delete from unsubs where hash=%s', ss)
  return l
  
def anonymousAnalytics(email, unsubhash, success=False):
  digest = hashEmail(email)
  
  now = str(datetime.datetime.now())
  results = fetch('select unsubhash, success from anonymousanalytics where unsubhash=%s', (unsubhash))
  success = int(success)
  if results:
    if int(results[0][1]) == 0 and success:
      commit('update anonymousanalytics set success=1 where unsubhash=%s', (unsubhash))
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
  ll = getFive()
  log.log(ll)
  if not ll:
    return
  browser = selenium.getBrowser()
  for uns in ll:
    log.log(uns)
    res = unsubscribe(uns, browser)
    if not res:
      log.log('failed confirmation', uns)
      addEmailToSqlAnalytics(uns,False)
    else:
      log.log('confirmed unsub')
      commit('insert into usercount (another) values (1)')
      addEmailToSqlAnalytics(uns,True)
    browser = selenium.refreshBrowser(browser)

def unsubscribe(unsub, browser):
  return selenium.processPage(unsub,browser)
  
def mainMaster(wipe=False):
  if wipe:
    schema.wipe()
  mail =  gmail.connect()
  log.log('print analytics total, successful, all broken')
  results = fetch('select count(*) from analytics')
  log.log('total', results)
  results = fetch('select count(*) from analytics where success=1')
  log.log('successful', results)
  results = fetch('select email, url from analytics where success=0')
  log.log(results)
  
  it = 0
  while True:
    it += 1
    log.log('reading email')
    uss = None
    try:
      uss = gmail.readEmailFromGmail(mail)
    except Exception as e:
      log.log('exception', e)
      if it % 10 == 0:
        mail = gmail.connect()
    log.log('handling unsubs')
    results = fetch('select * from unsubs')
    log.log(results)
    results = fetch('select * from readmail')
    log.log(results)
    try:
      handleDB(uss)
    except Exception as e:
      log.log('exception', e)
    sleeplen = 20
    log.log('sleeping for '+str(sleeplen))
    if it % 1000 == 0:
      mail = gmail.connect()
    time.sleep(sleeplen)

def getAnalyticsForEmail(email):
  digest = hashEmail(email)
  results = fetch('select count(*) from anonymousanalytics where emailhash=%s', digest)
  total = results[0][0]
  results = fetch('select count(*) from anonymousanalytics where emailhash=%s and success=1', digest)
  successful = results[0][0]
  return successful, total

def printAnalytics():
  schema.wipe()
  log.log('print analytics total, successful, all broken')
  results = fetch('select count(*) from analytics')
  log.log('total', results)
  results = fetch('select count(*) from analytics where success=1')
  log.log('successful', results)
  results = fetch('select email, url from analytics where success=0')
  log.log(results)
  log.log('success / total for william.k.dvorak')
  log.log(getAnalyticsForEmail('william.k.dvorak@gmail.com'))
    
def mainSlave():
  log.log('print analytics total, successful, all broken')
  results = fetch('select count(*) from analytics')
  log.log('total', results)
  results = fetch('select count(*) from analytics where success=1')
  log.log('successful', results)
  results = fetch('select email, url from analytics where success=0')
  log.log(results)
  
  it = 0
  while True:
    it += 1
    uss = None
    log.log('handling unsubs')
    results = fetch('select * from unsubs')
    log.log(results)
    results = fetch('select * from readmail')
    log.log(results)
    try:
      handleDB(uss)
    except Exception as e:
      log.log('exception', e)
    sleeplen = 20
    log.log('sleeping for '+str(sleeplen))
    time.sleep(sleeplen)
    