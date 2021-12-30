# how to automate: https://datatofish.com/python-script-windows-scheduler/ or cloud solutions

import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}

url = {"gpu":"https://www.amazon.com/XFX-Radeon-1286MHz-Graphics-RX-570P8DFD6\
/dp/B077VX31FZ/ref=sr_1_2?dchild=1&keywords=rx+570&qid=1592422039&sr=8-2"}
# the \ can help you write code across lines
# to use multiple url's maybe put them all in a dictionary and do a for loop in check_price
target_price = {"gpu":160}
# idea for future improvement: calculate moving average instead of a somewhat arbitrary target price

def check_price(component):
	page = requests.get(url[component], headers = headers)
	soup = BeautifulSoup(page.content, 'lxml') 
	# cannot use html.parser, must use the other two (lxml or html5lib) bc the html doesn't work; I think this is because of Javascript in the browser
	# https://stackoverflow.com/questions/45494505/python-difference-between-lxml-and-html-parser-and-html5lib-with-beautifu?rq=1
	price = soup.find(id="priceblock_ourprice").get_text()
	name = soup.find(id="productTitle").get_text()
	# if there are a lot of spaces, you can use .strip()
	rounded_price = round(float(price[1:]))
	if rounded_price < target_price[component]:
		send_whatsapp(component)
def send_whatsapp(component):
	client = Client()
	whatsapp_sender = 'whatsapp:+14155238886'
	whatsapp_recipient = 'whatsapp:' + os.environ.get('my_phone_number')
	client.messages.create(body='Price of '+component+' has dipped below '+str(target_price[component]), from_=whatsapp_sender, to=whatsapp_recipient)

check_price("gpu")