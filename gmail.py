# https://stackoverflow.com/questions/1777264/using-python-imaplib-to-delete-an-email-from-gmail

import imaplib
from sql import commit
from sql import fetch
import log

f = open('/auth/gmail.txt')
both = f.read().split('\n')
f.close()
address = both[0]
password = both[1]
imap = "imap.gmail.com"
port   = 993

import time
import imaplib
import email

linkPositives = ['unsubscribe', 'remove', 'stop receiv']

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
    return None
  httpIndex = body.find('http', index)
  if httpIndex - index > 100:
    return None
  endIndex = body.find('>', httpIndex + 2)
  url = body[httpIndex:endIndex]
  return url
  
  
def getCandidates(body):
  lower = body.lower()
  length = len(lower)
  
  candidates = set()
  for lp in linkPositives:
    start = lower.find('content-type')
    while start != -1:
      c = getCandidate(body, lp, start)
      if c:
        candidates.add(c)
      start = lower.find(lp, start+1)-3
  return candidates
    
  
def processOne(mail, i):
  try:
    unused, data = mail.fetch(i, '(RFC822)' )
  except Exception as e:
    log.log(e)
    
  for response_part in data:
    if not isinstance(response_part, tuple):
      continue
      
    msg = email.message_from_string(response_part[1])
    fromAddress = getAddress(msg)
    
    body = msg.as_string()
    body = actual.replace('=\r\n','')
    
    candidates = getCandidates(body)
    for c in candidates:
      commit('insert into unsubs (url, email) values (%s, %s)', (c, fromAddress))

def read_email_from_gmail():
  data = None
  try:
    # login and get emails
    mail = imaplib.IMAP4_SSL(imap)
    mail.login(address,password)
    mail.select('inbox')

    unused, data = mail.search(None, 'ALL')
  except Exception as e:
    log.log(e)
    
  if not data:
    return
    
  mail_ids = data[0]
  id_list = mail_ids.split()   
  first_email_id = int(id_list[0])
  latest_email_id = int(id_list[-1])
  
  # track read in db
  emails = fetch('select email from read')
  read = set()
  for e in emails:
    read.add(int(e[0]))
  processed = set()
  
  # process
  for i in range(first_email_id, latest_email_id):
    if i in read:
      continue
    processOne(mail, i)
    processed.add(i)
  
  # write read in db
  for i in processed:
    commit('insert into read (email) values (%s)', i)
    
#read_email_from_gmail()