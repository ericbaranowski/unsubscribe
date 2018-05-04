import time
import random
import log
import signal

delay = .5
pageDelay = 3
pageTimeout = 15

checkboxPositives = ['remove', 'stop', 'unsub', 'off', 'opt out', 'not interested', 'no email']
buttonPositives = ['remove', 'stop', 'unsub', 'go', 'submit', 'click', 'opt out', 'yes', 'update', 'don\'t send me any', 'don\'t send any', 'stop sending', 'confirm', 'do not email', 'block all emails', 'permanently remove']
radioPositives = ['all', 'none', 'complete','no email']
shortConfirmPositives = ['successfully unsubscribed', 'confirmed unsubscribed', 'now unsubscribed', 'unsubscribe successful', 'successfully removed', 'unsubscribe confirmation','unsubscribed successfully', 'been unsubscribed', 'have been unsubscribe','email unsubscribe', 'preferences have been update', 'sorry to see you go','you\'re unsubscribe','you are unsubscribe', 'unsubscribed now']
confirmPositives = ['unsubscribed', 'success', 'thank you', 'updated', 'have removed', 'request has been processed', 'request processed', 'unsubscribe confirm', 'has been remove', 'have been remove','deleted'] + shortConfirmPositives

js_code = "return document.getElementsByTagName('html')[0].innerHTML;"

getDone = False

def handler(signum, frame):
  # YUCK -- native page load timeout in selenium is garbage and doesnt work
  global getDone
  if getDone:
    return
  log.warn('browser timed out')
  raise Exception('browser timed out')

def browserGetPage(browser,url): 
  signal.signal(signal.SIGALRM, handler)
  signal.alarm(pageTimeout)
  try:
    global getDone
    getDone = False
    browser.get(url)
    getDone = True
    time.sleep(pageDelay)
  except Exception as e:
    log.warn(e)
    
  return browser
    
  
def getBrowser():
  # import subprocess
  # try:
  #   subprocess.call(['rm -rf /tmp'])
  # except:
  #   log.info('got here')
  log.info('getting browser')
  from pyvirtualdisplay import Display
  from selenium import webdriver
  display = Display(visible=0, size=(800, 600))
  display.start()
  # capabilities = webdriver.DesiredCapabilities().FIREFOX
  # capabilities["marionette"] = False
  # browser = webdriver.Firefox(capabilities=capabilities)
  browser = webdriver.Firefox()
  log.info('got browser')
  #browser.implicitly_wait(10)
  return browser, display

def getPageBody(browser):
  body = browser.execute_script(js_code)
  if body:
    return body
  return browser.page_source

def processPage(unsub, browser):
  try:
    browser = process(unsub, browser)
    if browser == 'done':
      return True
    if browser:
      time.sleep(pageDelay)
      body = getPageBody(browser)
      if not body:
        log.info('did not get a confirm page')
        return False
      body = body.lower()
      if  any(pos in body for pos in confirmPositives):
        log.info('confirm by confirmPositives')
        return True
      log.info('no confirmed unsub,', body[:50])
    log.info('browser was false')
    return False
  except Exception as e:
    log.info('exception'+ str(e))
  return False

def getText(child):
  text = child.text.lower()
  if not text or len(text) < 3:
    text = child.get_attribute('alt')
    if text:
      text = text.lower()
  if not text or len(text) < 3:
    text = child.get_attribute('value')
    if text:
      text = text.lower()
  if not text or len(text) < 3:
    text = child.get_attribute('name')
    if text:
      text = text.lower()
  if not text or len(text) < 3:
    text = child.get_attribute('onclick')
    if text:
      text = text.lower()
  if not text or len(text) < 3:
    return None
  return text
  
def process(unsub, browser):
  url = unsub.url
  email = unsub.email
  browser = browserGetPage(browser,url)
  
  body = getPageBody(browser)
  body = body.lower()
  if any(pos in body for pos in shortConfirmPositives):
    log.info('short positive confirm')
    return 'done'

  log.info('main frame')
  ans = processFrame(browser, email)
  if ans:
    return ans


  browser = browserGetPage(browser,url)
  
  frames = browser.find_elements_by_tag_name('iframe')
  frames = list(reversed(frames))
  numFrames = len(frames)
  for i in range(numFrames):
    frame = frames[i]
    log.info('next frame')
    browser.switch_to.frame(frame)
    time.sleep(pageDelay)
    ans = processFrame(browser, email)
    if ans:
      return ans
    # refresh frames list

    browser = browserGetPage(browser,url)
    frames = browser.find_elements_by_tag_name('iframe')
    frames = list(reversed(frames))
  return ans
  
def doFun(fun, args=None):
  try:
    if not args:
      fun()
      return True
    if args:
      fun(args)
      return True
  except Exception as e:
    log.info('exception', e)
  return False

def selects(browser):
  selects = browser.find_elements_by_xpath("//select")
  for select in selects:
    children = select.find_elements_by_xpath("./option")
    clicked = False
    for child in children:
      text = getText(child)
      if any(pos in text for pos in radioPositives):
        if doFun(child.click):
          clicked = True
          log.info('clicked select')
    if not clicked and children:
      if doFun(children[-1].click):  # click the last option, usually unsub all
        log.info('clicked select defaulted last')

def radios(browser, unused):
  lists = []
  radios = browser.find_elements_by_xpath("//input[contains(@type, 'radio')]")
  currentList = []
  currentName = None
  if radios:
    currentName = radios[0].get_attribute('name')
  for radio in radios:
    name = radio.get_attribute('name')
    if name != currentName:
      lists.append(currentList)
      currentList = []
      currentName = name
    currentList.append(radio)
  lists.append(currentList)
  for l in lists:
    clicked = False
    for radio in l:
      text = getText(radio)
      if any(pos in text for pos in radioPositives):
        if doFun(radio.click):
          clicked = True
          log.info('clicked radio')
    if not clicked and l:
        if doFun(l[-1].click): # click the last option, usually unsub all
          log.info('clicked radio defaulted last')

def atags(browser, unused):
  aTags = browser.find_elements_by_xpath("//a")
  aTags = reversed(aTags)
  for aTag in aTags:
    text = getText(aTag)
    if not text:
      continue
    if not aTag.is_displayed() or not aTag.is_enabled():
      continue
    if any(pos in text for pos in buttonPositives):
      time.sleep(delay)
      funn = aTag.submit
      if aTag.get_attribute('onclick'):
        funn = aTag.click
      if doFun(funn):
        log.info('a tag submitted')
        return browser
  return None

def buttons(browser, unused):
  buttonTags = browser.find_elements_by_xpath("//button")
  buttonTags = reversed(buttonTags)
  for buttonTag in buttonTags:
    text = getText(buttonTag)
    if not text:
      continue
    if not buttonTag.is_displayed() or not buttonTag.is_enabled():
      continue
    if any(pos in text for pos in buttonPositives):
      time.sleep(delay)
      if doFun(buttonTag.click):
        log.info('clicked button')
        return browser
  return None

def onclicks(browser, unused):
  clickTags = browser.find_elements_by_xpath("//*[@onclick]")
  clickTags = reversed(clickTags)
  for clickTag in clickTags:
    text = getText(clickTag)
    if not text:
      continue
    if not clickTag.is_displayed() or not clickTag.is_enabled():
      continue
    if any(pos in text for pos in buttonPositives):
      time.sleep(delay)
      jss = clickTag.get_attribute('onclick')
      browser.execute_script(jss)
      return browser
  return None

def forms(browser, email):
  forms = browser.find_elements_by_xpath("//form")
  forms = reversed(forms)  
  
  for form in forms:
    children = form.find_elements_by_xpath(".//input")
    for child in children:
      text = getText(child)
      if not child.is_displayed() or not child.is_enabled():
        continue
      if child.tag_name == "input":
        if child.get_attribute('type') == "text":
          doFun(child.clear)
          doFun(child.send_keys,email)
          continue
        if not text:
          continue
        if child.get_attribute('type') == "checkbox":
          if any(pos in text for pos in checkboxPositives) and not child.is_selected():
            if doFun(child.click):
              log.info('clicked checkbox')
          elif not any(pos in text for pos in checkboxPositives) and child.is_selected():
            if doFun(child.click):
              log.info('unclicked checkbox')
          continue
        if child.get_attribute('type') == "button" and any(pos in text for pos in buttonPositives):
          time.sleep(delay)
          if doFun(child.submit):
            return browser
          continue
        if child.get_attribute('type') == "image" and any(pos in text for pos in buttonPositives):
          time.sleep(delay)
          if doFun(child.submit):
            return browser
          continue
        if child.get_attribute('type') == "submit" and any(pos in text for pos in buttonPositives):
          time.sleep(delay)
          doFun(child.submit)
          return browser
    children = form.find_elements_by_xpath(".//button")
    for child in children:
      text = getText(child)
      if not text:
        continue
      if child.tag_name == "button" and any(pos in text for pos in buttonPositives):
        time.sleep(delay)
        if doFun(child.submit):
          return browser
        continue
    children = form.find_elements_by_xpath(".//a")
    for child in children:
      text = getText(child)
      if child.tag_name == "a" and any(pos in text for pos in buttonPositives):
        time.sleep(delay)
        funn = child.submit
        if child.get_attribute('onclick'):
          funn = child.click
        if doFun(funn):
          log.info('submits a tag')
          return browser
        continue
  return None

def processFrame(browser, email):  
  funs = [radios, forms, atags, buttons, onclicks]
  for ff in funs:
    result = None
    try:
      result = ff(browser, email)
    except Exception as e:
      log.info('exception', e)
    if result:
      return browser
    
  return None

def subbbmit():
  submitTags = browser.find_elements_by_xpath("//*[@onsubmit]")
  submitTags = reversed(submitTags)
  for submitTag in submitTags:
    time.sleep(delay)
    jss = submitTag.get_attribute('onsubmit')
    browser.execute_script(jss)
    return browser
    
def clickRecursive(elem):
  children = elem.find_elements_by_xpath(".//*")
  children = [elem] + children
  for child in children:
    ans = doFun(child.click)
    if ans:
      return True
  return False

def closeBrowser(browser,display):
  browser.close()
  display.stop()
  time.sleep(2)

def refreshBrowser(browser,display):
  body = ''
  try:
    url = 'https://www.google.com/search?q=check+browser'
    browser = browserGetPage(browser,url)
    body = getPageBody(browser).lower()
  except Exception as e:
    log.warn('refreshing browser', str(e))
  if 'whatsmybrowser.org' not in body:
    closeBrowser(browser,display)
    browser,display = getBrowser()
  return browser,display

