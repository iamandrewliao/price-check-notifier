import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}

url = {"gpu":"https://www.amazon.com/XFX-Radeon-1286MHz-Graphics-RX-570P8DFD6\
/dp/B077VX31FZ/ref=sr_1_2?dchild=1&keywords=rx+570&qid=1592422039&sr=8-2"}
# the \ can help you write code across lines
# to use multiple url's maybe put them all in a dictionary and do a for loop in check_price

url = {"Amazon": f"https://smile.amazon.com/s?k={part}&crid=2PWKVVFDU11SH&sprefix=570%2Caps%2C62&ref=nb_sb_noss_1",
	   "Newegg": f"https://www.newegg.com/p/pl?d={part}"}

def newegg():
	gpu = input("What part are you searching for? ")

	pages_raw = doc.find(class_="list-tool-pagination-text").strong #finds the page number (in the form "x/y" e.g. 1/4)
	pages = int(str(pages_raw).split("/")[-2].split(">")[:-1]) #parses "x/y" to find the total number of pages
	for i in range(1, pages+1):
		url = f"https://www.newegg.com/p/pl?d={gpu}&N=100007709&isdeptsrh=1&page={i}"
		page = requests.get(url).text
		doc = BeautifulSoup(page, "html.parser")

# I want this to return to me product names and their links and prices

target_price = {"gpu":160}

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