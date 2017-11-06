#http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement
# switch to implicitly wait

path = '/Users/williamdvorak/Desktop/unsubscribe/git/'

#import sys
#sys.path.insert(0, path)
##print sys.path
import os
os.environ["PATH"] += os.pathsep +  path

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
pageDelay = 3

checkboxPositives = ['remove', 'stop', 'unsub', 'off', 'opt out']
buttonPositives = ['remove', 'stop', 'unsub', 'go', 'submit', 'click', 'opt out']
radioPositives = ['all', 'none', 'complete']
confirmPositives = ['unsubscribed', 'success', 'thank']
	
def GetBrowser():
	log.log('getting browser')
	display = Display(visible=0, size=(800, 600))
	display.start()
	browser = webdriver.Firefox()
  browser.implicitly_wait(.1)
	log.log('got browser')
	return browser
	
def ProcessPage(unsub, browser):
	browser = process(unsub, browser)
	if browser:
		time.sleep(pageDelay)
		result = browser.page_source.encode("utf-8")
		if result:
			log.log('got result')
		if  any(pos in result for pos in confirmPositives):
			return True
	return False

#def click(child):
#	try:
#		child.click()
#		return browser
#	except Exception as e:
#		log.log('exception', e
	
def process(unsub, browser):
	url = unsub.url
	email = unsub.email
	browser.get(url)
	time.sleep(pageDelay)
	result = browser.page_source.encode("utf-8")
	
	js_code = "return document.getElementsByTagName('html')[0].innerHTML;"
	your_elements = browser.execute_script(js_code)
	log.log(your_elements)
	log.log(dir(browser))
	log.log(browser.current_url)
	
	forms = browser.find_elements_by_xpath("//form")
	for form in forms:
		children = form.find_elements_by_xpath("//*")
		for child in children:
			text = child.text.lower()
			if not child.is_displayed() or not child.is_enabled():
				continue
			if child.tag_name == "input":
				log.log('bllllahh',child.tag_name, text, child.get_attribute('type'))
				if child.get_attribute('type') == "text":
					try:
						child.send_keys(email)
					except Exception as e:
						log.log('exception', e)
				if child.get_attribute('type') == "checkbox":
					if any(pos in text for pos in checkboxPositives) and not child.is_selected():
						try:
							child.click()
						except Exception as e:
							log.log('exception', e)
				if child.get_attribute('type') == "radio":
					if any(pos in text for pos in radioPositives) and not child.is_selected():
						try:
							child.click()
						except Exception as e:
							log.log('exception', e)
				if child.get_attribute('type') == "submit" and any(pos in text for pos in buttonPositives):
					time.sleep(delay)
					try:
						child.submit()
						return browser
					except Exception as e:
						log.log('exception', e)
			if child.tag_name == "button" and any(pos in text for pos in buttonPositives):
				time.sleep(delay)
				try:
					child.submit()
					return browser
				except Exception as e:
					log.log('exception', e)
			if child.tag_name == "a" and any(pos in text for pos in buttonPositives):
				time.sleep(delay)
				try:
					child.submit()
					return browser
				except Exception as e:
					log.log('exception', e)
	aTags = browser.find_elements_by_xpath("//a")
	for aTag in aTags:
		text = aTag.text.lower()
		log.log('bllllahh',aTag.tag_name, text, aTag.get_attribute('type'))
		if any(pos in text for pos in buttonPositives):
			time.sleep(delay)
			try:
				aTag.submit()
				return browser
			except Exception as e:
				log.log('exception', e)
	buttonTags = browser.find_elements_by_xpath("//button")
	for buttonTag in buttonTags:
		text = buttonTag.text.lower()
		log.log('bllllahh',buttonTag.tag_name, text, buttonTag.get_attribute('type'))
		if any(pos in text for pos in buttonPositives):
			time.sleep(delay)
			try:
				buttonTag.click()
				return browser
			except Exception as e:
				log.log('exception', e)
	return None
	
def CheckBrowser(browser):
	return True
						
	