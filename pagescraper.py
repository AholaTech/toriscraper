# !/usr/bin/python

import requests
import datetime
import config #configuration file
from lxml import html

current_time = datetime.datetime.now()
#print(datetime.datetime.now().time())

if(current_time.hour == config.start_hour and current_time.minute < (config.start_minute + 2)):
    first_run_of_day = True
else:
    first_run_of_day = False

#print(current_Time.minute)

page = requests.get(config.url)
root = html.fromstring(page.content)

if(config.allow_stores):
    items = root.xpath('//div[contains(@id,"item_"]')
else:
    items = root.xpath('//div[contains(@id,"item_") and not(contains(.//div//span,"KAUPPA"))]')
    #items = root.xpath('//div[contains(@class,"item_row") and not(contains(.//div//span,"KAUPPA"))]')
    #items = root.xpath('//div[@class="item_row" and not(contains(.//div//span,"KAUPPA"))]')

for num in range(len(items)):
    title=items[num].xpath('.//a[contains(@tabindex,50)]/text()')
    [date,time]=items[num].xpath('.//*[contains(@class,"date_image")]/text()')
    date=date.strip()
    time=time.strip()
    [hour,minute]=time.split(":")
    hour=int(hour)
    minute=int(minute)
    price=items[num].xpath('.//*[contains(@class,"list_price ineuros")]/text()')
    
    if(first_run_of_day):
        if((date == "tänään" or date == "eilen") and abs((hour*60+minute)-(current_time.hour*60+current_time.minute)) <= (config.start_hour+(24-config.end_hour))*60-config.end_minute):
            print('New item since last run of yesterday')
            print(title)
            print(price)
    else:
        if(date == "tänään" and abs((hour*60+minute)-(current_time.hour*60+current_time.minute)) <= config.interval):
            print('New item')
            print(title)
            print(price)
            
print("Run complete.")
