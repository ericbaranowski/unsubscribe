from sql import fetch
from sql import commit
import time
import sel as selenium
import gmail
import schema
import log

class UnSub:
  def __init__(self, url, email):
    self.url = url
    self.email = email
  def __repr__(self):
    return self.url + "  " + self.email

def refreshList():
  results = fetch('select url, email from unsubs')
  l = list()
  for r in results:
    l.append(UnSub(r[0], r[1]))
  return l
  
def deleteEntry(unsub):
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
    else:
      log.log('confirmed unsub')
      commit('insert into usercount (another) values (1)')
    deleteEntry(uns)
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
  
  while True:
    log.log('reading email')
    uss = None
    try:
      uss = gmail.readEmailFromGmail()
    except Exception as e:
      log.log('exception', e)
    log.log('handling unsubs')
    results = fetch('select * from unsubs')
    log.log(results)
    results = fetch('select * from readmail')
    log.log(results)
    try:
      handleDB(uss)
    except Exception as e:
      log.log('exception', e)
    time.sleep(5)
    
main()

#todo
#get email from account, add links to queue
#parse email as html
#fill out form and submit
#delete email from account