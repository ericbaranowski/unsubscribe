from sql import fetch
from sql import commit
import time
import sel as selenium
import gmail
import schema
import log
import hashlib
import datetime

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
  
def anonymousAnalytics(email, table):
  email = email.lower()
  m = hashlib.sha256()
  m.update(email)
  digest = m.hexdigest()
  
  now = str(datetime.datetime.now())
  results = fetch('select stamp from '+table+' where hash=%s', (digest))
  if results:
    commit('update '+table+' set stamp=%s where hash=%s', (now, digest))
  else:
    commit('insert into '+table+' (hash, stamp) values (%s, %s)', (digest, now))
  
def fullAnalytics(email, url, success):
  s = int(success)
  commit('insert into analytics (email, url, success) values (%s, %s, %s)', (email, url, s))
    
def addEmailToSqlAnalytics(email, url=None, success=False):
  table = 'emailhashestotal'
  anonymousAnalytics(email, table)
  if success:
    table = 'emailhashespositive'
    anonymousAnalytics(email, table)
  if url:
    fullAnalytics(email, url, success)
    
  
def deleteEntry(unsub, alll=False):
  if alll:
    commit('delete from unsubs where hash=%s',(unsub.hashh))
  else:
    commit('delete from unsubs where url=%s and email=%s',(unsub.url, unsub.email))
  
def handleDB(ll):
  if not ll:
    ll = refreshList()
  log.log(ll)
  if not ll:
    return
  browser = selenium.getBrowser()
  for uns in ll:
    log.log(uns)
    res = unsubscribe(uns, browser)
    if not res:
      log.log('failed confirmation', uns)
      addEmailToSqlAnalytics(uns.email,uns.url,False)
      deleteEntry(uns, False)
    else:
      log.log('confirmed unsub')
      commit('insert into usercount (another) values (1)')
      addEmailToSqlAnalytics(uns.email,uns.url,True)
      deleteEntry(uns, True)
    browser = selenium.refreshBrowser(browser)

def unsubscribe(unsub, browser):
  return selenium.processPage(unsub,browser)
  
def main(wipe=False):
  if wipe:
    schema.wipe()
  #commit('delete from unsubs where true')
  #gmail.readEmailFromGmail()
  #browser = selenium.getBrowser()
  #uns = UnSub('http://click.lyftmail.com/unsub_center.aspx?qs=da6bddaa337452c8861ca82f0125d1a97b5ca3e1797ce5cf1754ceb6de34f4221ad2231ac40b5b7d284f2d927b01b574869c6d3fdcde9361a2736ce552288b28d7c6704f16852dbc', 'william.k.dvorak@gmail.com')
  #commit('insert into unsubs (url, email) values (%s, %s)', (uns.url, uns.email))
  #print unsubscribe(uns, browser)
  #return
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
    
main()

#todo
#get email from account, add links to queue
#parse email as html
#fill out form and submit
#delete email from account
