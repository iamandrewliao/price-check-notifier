# price-check-notifier

## Description
-Web scrapes the price of an amazon product given a url (using BeautifulSoup and requests)  
-Notifies me via WhatsApp (through Twilio API) if the price dips below a set target price  
-should be automated to run every given time interval (cron for Unix, scheduled tasks for Windows)

## Potential updates
-Track moving average instead of setting a target price
