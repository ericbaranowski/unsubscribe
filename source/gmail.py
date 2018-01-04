# https://stackoverflow.com/questions/1777264/using-python-imaplib-to-delete-an-email-from-gmail

import imaplib
from sql import commit
from sql import fetch
import log
import time
import imaplib
import email
import datetime
from datetime import timedelta
import string
import random

linkPositives = ['unsubscribe', 'remove', 'stop receiv', 'opt-out', 'opt out','not to receiv', 'not receiv']

def newHash():
  lets = string.ascii_letters[:26] + string.digits
  ans = ''
  for i in range(8):
    ans += random.choice(lets)
  return ans

class UnSub:
  def __init__(self, url, email, hashh):
    self.url = url
    self.email = email
    self.hashh = hashh
  def __repr__(self):
    return self.url + "  " + self.email

def writeFile(s):
  f = open('email.html','w')
  f.write(s)
  f.close()

def getAddress(msg):
  fromAddressFull = str(msg['from'])
  start = fromAddressFull.find('<') + 1
  end = fromAddressFull.find('>')
  if end == -1:
    return fromAddressFull
  return fromAddressFull[start:end]
  
def getCandidate(body, keyword, start):
  lower = body.lower()
  index = lower.find(keyword,start)
  if index == -1:
    return None, start
  httpIndex = body.find('http', index)
  if httpIndex - index > 100:
    return None, start
  endKarat = body.find('>', httpIndex + 2)
  endQuote = body.find('"', httpIndex + 2)
  endIndex = min(endKarat, endQuote)
  if endQuote == -1:
    endIndex = endKarat
  url = body[httpIndex:endIndex]
  return url, index
  
def getCandidateNearby(body, keyword, start):
  lower = body.lower()
  index = lower.find(keyword,start)
  if index == -1:
    return None, start
  searchArea = body[index-600:index+600]
  for lp in linkPositives:
    if lp in searchArea:
      index = min(index, lower.find(lp, start))
  httpIndex = body.find('http', index)
  if httpIndex - index > 100:
    return None, start
  endKarat = body.find('>', httpIndex + 2)
  endQuote = body.find('"', httpIndex + 2)
  endIndex = min(endKarat, endQuote)
  if endQuote == -1:
    endIndex = endKarat
  url = body[httpIndex:endIndex]
  return url, index
  
def getCandidates(body):
  lower = body.lower()
  length = len(lower)
  
  candidates = list()
  end = lower.rfind('content-type: text/html')
  cccc = lower.count('content-type: text/html')
  if cccc > 1:
    log.info('more than one text/html', cccc, lower)
    
  for lp in linkPositives:
    start = lower.find('content-type')
    while start > 5:
      c, start = getCandidate(body, lp, start)
      if c:
        candidates.append(c)
      start = lower.find(lp, start+1,end)
  return set(candidates)
    
  
def processOne(mail, i, actuallyCommit=False):
  try:
    unused, data = mail.fetch(i, '(RFC822)' )
  except Exception as e:
    log.info(e)
  hashh = newHash()
  for response_part in data:
    if not isinstance(response_part, tuple):
      continue
      
    msg = email.message_from_string(response_part[1])
    fromAddress = getAddress(msg)
    
    body = msg.as_string()
    body = body.replace('=\r\n','')
    body = body.replace('=3D','=')

    if fromAddress == 'dangelofamily@optonline.net' or fromAddress == 'william.k.dvorak@gmail.com':
      log.info(body)
    
    candidates = getCandidates(body)
    log.info('candidates', candidates)
    ccs = list()
    for c in candidates:
      if actuallyCommit:
        commit('insert into unsubs (hash, url, email) values (%s, %s, %s)', (hashh, c, fromAddress))
        ccs.append(UnSub(c, fromAddress, hashh))
    return ccs

def connect():
  mail = None
  try:
    f = open('/auth/gmail.txt')
    both = f.read().split('\n')
    f.close()
    address = both[0]
    password = both[1]
    imap = "imap.gmail.com"
  
    mail = imaplib.IMAP4_SSL(imap)
    mail.login(address,password)
  except Exception as e:
    log.info('exception connecting to gmail', e)
  return mail

def readEmailFromGmail(mail):
  data = None
  try:
    log.info('login and get emails')

    mail.select('inbox')
    now = (datetime.datetime.now()-timedelta(days=100)).strftime('%d-%b-%Y')
    if now[0] == '0':
      now = now[1:]
    log.info('(SINCE %s)' % now)
    unused, data = mail.search(None, '(SINCE %s)' % now)
  except Exception as e:
    log.info(e)
    
  if not data:
    log.info('no new emails %s', str(mail))
    return

  uss = list()
  mail_ids = data[0]
  
  if not mail_ids:
    return uss
  id_list = mail_ids.split()   
  first_email_id = int(id_list[0])
  latest_email_id = int(id_list[-1])
  
  log.info('track read in db')
  emails = fetch('select email from readmail')
  read = set()
  for e in emails:
    read.add(int(e[0]))
  processed = set()
  
  log.info('process')
  for i in range(first_email_id, latest_email_id+1):
    if int(i) in read:
      pass # TODO switch to continue
    candidates = processOne(mail, i)
    uss.extend(candidates)
    processed.add(i)
  
  log.info('write read in db')
  for i in processed:
    commit('insert into readmail (email) values (%s)', i)
  return uss
    
#readEmailFromGmail()