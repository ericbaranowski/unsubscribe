
from pyvirtualdisplay import Display
from selenium import webdriver

import time


js_code = "return document.getElementsByTagName('html')[0].innerHTML;"

def getPageBody(browser):
  body = browser.execute_script(js_code)
  if body:
    return body
  return browser.page_source
  

def closeBrowser(browser,display):
  browser.close()
  display.stop()
  time.sleep(2)
  
def getBrowser():
  display = Display(visible=0, size=(800, 600))
  display.start()

  browser = webdriver.Firefox()
  return browser, display

def testBrowser(browser):
  browser.set_page_load_timeout(20)
  browser.get('https://www.google.com/search?q=check+browser')
  time.sleep(2)
  body = getPageBody(browser).lower()
  if 'whatsmybrowser.org':
    print 'good'
  else:
    print 'broken'

def  main():
  for i in range(30):
    print i
    browser, display = getBrowser()
    testBrowser(browser)
    closeBrowser(browser,display)
  
main()