# https://stackoverflow.com/questions/1777264/using-python-imaplib-to-delete-an-email-from-gmail

import imaplib
from sql import commit

address	= "asdfUnsubscribe@gmail.com"
f = open('/auth/gmail.txt')
password = f.read().split('\n')[1]
imap = "imap.gmail.com"
port	 = 993

mail = imaplib.IMAP4_SSL(imap)
mail.login(address,password)

mail.select('inbox')



import time
import imaplib
import email

buttonPositives = ['unsubscribe', 'remove', 'stop']

def writeFile(s):
	f = open('email.html','w')
	f.write(s)
	f.close()
	

def read_email_from_gmail():
	try:
		mail = imaplib.IMAP4_SSL(imap)
		mail.login(address,password)
		mail.select('inbox')

		type, data = mail.search(None, 'ALL')
		mail_ids = data[0]

		id_list = mail_ids.split()	 
		first_email_id = int(id_list[0])
		latest_email_id = int(id_list[-1])


		for i in range(latest_email_id,first_email_id, -1):
			typ, data = mail.fetch(i, '(RFC822)' )

			for response_part in data:
				if isinstance(response_part, tuple):
					msg = email.message_from_string(response_part[1])
					fromAddressFull = msg['from']
					start = fromAddressFull.find('<') + 1
					end = fromAddressFull.find('>')
					fromAddress = fromAddressFull[start:end]
					b = msg
					actual = msg.as_string()
					body = msg.as_string().lower()
					body = body.replace('=\r\n','')
					actual = actual.replace('=\r\n','')
					url = None
					for bp in buttonPositives:
						start = body.find('content-type')
						index = body.find(bp,start)
						if index == -1:
							continue
						httpIndex = body.find('http', index)
						if httpIndex - index > 100:
							continue
						endIndex = body.find('>', httpIndex + 2)
						url = actual[httpIndex:endIndex]
						commit('insert into unsubs (url, email) values (%s, %s)', (url, fromAddress))
	except Exception, e:
		print str(e)
		
#read_email_from_gmail()