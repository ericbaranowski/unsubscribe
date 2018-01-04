import log
import time

con = None
local = False

if not local:
  import MySQLdb as mdb
  import time

  f = open('/auth/sql.txt')
  lines = f.readlines()
  f.close()
  user = lines[0][:-1]
  password = lines[1][:-1]
  ip = lines[2][:-1]

def closeDB():
  con.close()
  
def resetCon():
  global con
  time.sleep(.5)
  con = mdb.connect(ip, user, password, 'unsubscribe')
  con.charset='utf8'

def fetch(query, ps=None, tryNum=0):
  params = None
  if ps:
    if type(ps) == list or type(ps) == tuple:
      pass
    else:
      ps = (str(ps),)
    params = []
    for param in ps:
      t = type(param)
      if t == str or t == unicode:
        params.append(str(param.encode('utf-8', 'replace')))
      elif t == int or t == bool:
        params.append(param)
      else:
        params.append(str(param))
  log.info(params)
  if tryNum == 3:
    return []
  log.debug('Fetch query:'+ query + str(params))
  rows = []
  try:
    with con:
      cur = con.cursor()
      cur.execute(query, params)
      rows = cur.fetchall()
      cur.close() 
  except Exception as e:
    log.warn('Fetch failed query:%s, error:%s'% (query + str(params), str(e)) + 'tryyyyy' + str(tryNum))
    if 'Commands out of sync' in str(e) or 'MySQL server has gone away' in str(e):
      resetCon()
      return fetch(query, params, tryNum+1)
  ans = []
  for row in rows:
    inner = []
    for field in row:
      temp = field
      if type(field) == str:
        temp = field.decode('utf-8', 'replace')
      inner.append(temp)
    ans.append(inner)
  return ans
  
def commit(query, ps=None, tryNum=0):
  params = None
  if ps:
    if type(ps) == list or type(ps) == tuple:
      pass
    else:
      ps = (str(ps),)
    params = []
    for param in ps:
      t = type(param)
      if t == str or t == unicode:
        params.append(str(param.encode('utf-8', 'replace')))
      elif t == int or t == bool:
        params.append(param)
      else:
        params.append(str(param))
  if tryNum == 3:
    return False
  log.debug('Commit query:'+ query + str(params))
  try:
    with con:
      cur = con.cursor()
      cur.execute(query, params)
      con.commit()
      cur.close() 
      return True
  except Exception as e:
    log.warn('Commit failed query:%s, error:%s' % (query + str(params), str(e)) + 'tryyyyy' + str(tryNum))
    if 'Commands out of sync' in str(e) or 'MySQL server has gone away' in str(e):
      resetCon()
      return commit(query, params, tryNum+1)
  return False
  
if not local:
  resetCon()