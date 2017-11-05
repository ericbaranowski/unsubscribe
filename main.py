from sql import fetch
from sql import commit
import time
import sel as selenium
import gmail
import schema

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
	
def handleDB():
	ll = refreshList()
	print ll 
	browser = selenium.GetBrowser()
	for uns in ll:
		uns.url = 'https://www.massdrop.com/unsubscribe?eid=ad7d3e0d349a19dd5896706156ab0974e229a74fac5db955142efb277336b3075d27eff71c114f90&utm_source=Iterable&utm_medium=email&utm_campaign=cm_v1_mixed_ftp_%5B%5Burl%5D%5D&referer=39SRGY&mode=guest_open&iterableCampaignId=194395&iterableTemplateId=278839'
		print unsubscribe(uns, browser)
		#deleteEntry(uns)
		if not selenium.CheckBrowser(browser):
			browser = selenium.GetBrowser()
		break

def scrapeEmail():
	
	commit('insert into unsubs (url, email) values (%s, %s)', url, email)

def unsubscribe(unsub, browser):
	return selenium.ProcessPage(unsub,browser)
	
def main(wipe=False):
 if wipe:
  schema.setup()
 #commit('delete from unsubs where true')
 #gmail.read_email_from_gmail()
 #browser = selenium.GetBrowser()
 #uns = UnSub('https://mgmresorts.aprimo.com/Aprimo/EmailOptOut.aspx?A=f3262093d31295f65e1329f952f52a88f39fb83b76bc86ec&C=3&D=b9ca57b2fbe8cb42458807853387983f6a0f6be5ccdab113&Decode=0&Z=b333208886639fd5&E=bbc35e451a77b42bbc142b2cf70d488a0f04335a5a4e8916&M=b333208886639fd5&F=ca807df1a595466ed526855bcc5341c2&I=71f16b033e38cbb9a421a6fda82223b9&S=fb028f918e0199b01a07e466b95d9a5f&Test=0&Refresh=0', 'william.k.dvorak@gmail.com')
 #print unsubscribe(uns, browser)
 #return
 while True:
  handleDB()
  #time.sleep(5)
  break
		
main()

#todo
#get email from account, add links to queue
#parse email as html
#fill out form and submit
#delete email from account
