
#path = '/Users/williamdvorak/Desktop/unsubscribe/git/'

#import sys
#sys.path.insert(0, path)
##print sys.path
#import os
#os.environ["PATH"] += os.pathsep +  path

import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import log

from selenium.webdriver.common.keys import Keys
delay = .5
pageDelay = 5

checkboxPositives = ['remove', 'stop', 'unsub', 'off', 'opt out']
buttonPositives = ['remove', 'stop', 'unsub', 'go', 'submit', 'click', 'opt out', 'yes', 'update']
radioPositives = ['all', 'none', 'complete']
confirmPositives = ['unsubscribed', 'success', 'thank you', 'updated']
shortConfirmPositives = ['successfully unsubscribed', 'confirmed unsubscribed', 'now unsubscribed']

js_code = "return document.getElementsByTagName('html')[0].innerHTML;"
  
def getBrowser():
  log.log('getting browser')
  display = Display(visible=0, size=(80, 60))
  display.start()
  browser = webdriver.Firefox()
  #browser.implicitly_wait(1)
  log.log('got browser')
  return browser

def getPageBody(browser):
  return browser.execute_script(js_code)

def processPage(unsub, browser):
  browser = process(unsub, browser)
  if browser == 'done':
    return True
  if browser:
    time.sleep(pageDelay)
    body = getPageBody(browser)
    if not body:
      return False
      
    log.log('got result', body)
    body = body.lower()
    if  any(pos in body for pos in confirmPositives):
      return True
    log.log('no confirmed unsub,', body)
  return False

#def click(child):
# try:
#   child.click()
#   return browser
# except Exception as e:
#   log.log('exception', e

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
    return None
  return text
  
def getRadioName(radio):
  return radio.get_attribute('name')
  
def process(unsub, browser):
  url = unsub.url
  email = unsub.email
  browser.get(url)
  time.sleep(pageDelay)
  
  body = getPageBody(browser)
  body = body.lower()
  if any(pos in body for pos in shortConfirmPositives):
    return 'done'
  
  frames = browser.find_elements_by_tag_name('iframe')
  frames = reversed(frames)
  for frame in frames:
    log.log('next frame')
    browser.switch_to.frame(frame)
    time.sleep(pageDelay)
    ans = processFrame(browser, email)
    if ans:
      return ans
  log.log('main frame')
  browser.get(url)
  time.sleep(pageDelay)
  ans = processFrame(browser)
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
    log.log('exception', e)
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
    if not clicked and children:
      if doFun(children[-1].click): # click the last option, usually unsub all
        log.log('clicked select defaulted last')

def radios(browser):
  lists = []
  radios = browser.find_elements_by_xpath("//input[contains(@type, 'radio')]")
  currentList = []
  currentName = None
  if radios:
    currentName = getRadioName(radios[0])
  for radio in radios:
    name = getRadioName(radio)
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
          log.log('clicked radio')
    if not clicked and l:
        if doFun(l[-1].click): # click the last option, usually unsub all
          log.log('clicked radio defaulted last')

def ass(browser, unused):
  aTags = browser.find_elements_by_xpath("//a")
  aTags = reversed(aTags)
  for aTag in aTags:
    text = getText(aTag)
    if not text:
      continue
    if not aTag.is_displayed() or not aTag.is_enabled():
      continue
    log.log('bllllahh',aTag.tag_name, text, aTag.get_attribute('type'))
    if any(pos in text for pos in buttonPositives):
      time.sleep(delay)
      if doFun(aTag.submit):
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
    log.log('bllllahh',buttonTag.tag_name, text, buttonTag.get_attribute('type'))
    if any(pos in text for pos in buttonPositives):
      time.sleep(delay)
      if doFun(buttonTag.click):
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
    log.log('bllllahh',clickTag.tag_name, text, clickTag.get_attribute('type'))
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
    children = form.find_elements_by_xpath(".//*")
    for child in children:
      text = getText(child)
      if not child.is_displayed() or not child.is_enabled():
        continue
      log.log('bllllahh',child.tag_name, text, child.get_attribute('type'))  
      if child.tag_name == "input":
        if child.get_attribute('type') == "text":
          doFun(child.clear)
          doFun(child.send_keys,email)
          continue
        if not text:
          continue
        if child.get_attribute('type') == "checkbox":
          if any(pos in text for pos in checkboxPositives) and not child.is_selected():
            doFun(child.click)
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
      if not text:
        continue
      if child.tag_name == "button" and any(pos in text for pos in buttonPositives):
        time.sleep(delay)
        if doFun(child.submit):
          return browser
        continue
      if child.tag_name == "a" and any(pos in text for pos in buttonPositives):
        time.sleep(delay)
        if doFun(child.submit):
          return browser
        continue
  return None

def processFrame(browser, email):  
  funs = [forms, ass, buttons, onclicks]
  for ff in funs:
    result = ff(browser, email)
    if result:
      return browser
    
  return None

def subbbmit():
  submitTags = browser.find_elements_by_xpath("//*[@onsubmit]")
  submitTags = reversed(submitTags)
  for submitTag in submitTags:
    log.log('bllllahh',submitTag.tag_name, submitTag.get_attribute('type'))
    time.sleep(delay)
    jss = submitTag.get_attribute('onsubmit')
    browser.execute_script(jss)
    return browser
    
def clickRecursive(elem):
  children = elem.find_elements_by_xpath(".//*")
  children = [elem] + children
  for child in children:
    log.log(child.tag_name, getText(child))
    return doFun(child.click)
  return False

def refreshBrowser(browser):
  browser.get('https://www.google.com/search?q=check+browser')
  time.sleep(pageDelay)
  body = getPageBody(browser).lower()
  if 'whatsmybrowser.org' not in body:
    browser = getBrowser()
  return browser
  
            
  