import re
import requests
from bs4 import BeautifulSoup
import os
import datetime as dt

import urllib.request
from selenium import webdriver
from uuid import uuid4
import random
import string
from datetime import datetime

pip install chromedriver-py

driver = webdriver.Chrome("./chromedriver")
directory="./web"

***2021***
start_date = dt.date(2021, 1, 1)
end_date = dt.date(2021, 3, 16)
day_count = (end_date-start_date).days
date = start_date
date_str = date.strftime('%Y-%m/%d')
date_str2 = date.strftime('%Y%m%d')
day_count = (end_date - start_date).days
maxpage=8
page=1
page_count=maxpage-page

driver = webdriver.Chrome("./chromedriver")
for i in range(day_count):
    date += dt.timedelta(days=1)
    for page in range(page_count):
        page += 1
        site = 'http://paper.people.com.cn/rmrb/images/'+ str(date.strftime('%Y-%m/%d'))+"/"+str(page).zfill(2)+"/"+"rmrb"+ str(date.strftime('%Y%m%d'))+str(page).zfill(2)+".pdf"
        driver.get(site)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pdf_tags = soup.find_all('pdf')
        filename = str(date)+str(page).zfill(2)
        with open(os.path.join(directory, filename),'wb') as f:
            response = requests.get(site)
            f.write(response.content)

***2020/01/01-2020/07/01***
start_date = dt.date(2020, 1, 1)
end_date = dt.date(2020, 7, 1)
day_count = (end_date-start_date).days
date = start_date
date_str = date.strftime('%Y-%m/%d')
date_str2 = date.strftime('%Y%m%d')
day_count = (end_date - start_date).days
date = start_date
maxpage=8
page=1
page_count=maxpage-page

driver = webdriver.Chrome("./chromedriver")
for i in range(day_count):
    date += dt.timedelta(days=1)
    for page in range(page_count):
        page += 1
        site = 'http://paper.people.com.cn/rmrb/page/'+ str(date.strftime('%Y-%m/%d'))+"/"+str(page).zfill(2)+"/"+"rmrb"+ str(date.strftime('%Y%m%d'))+str(page).zfill(2)+".pdf"
        driver.get(site)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pdf_tags = soup.find_all('pdf')
        filename = str(date)+str(page).zfill(2)
        with open(os.path.join(directory, filename),'wb') as f:
            response = requests.get(site)
            f.write(response.content)

***2020/07/02-2020/12/31***
start_date = dt.date(2020, 7, 2)
end_date = dt.date(2020, 12, 31)
day_count = (end_date-start_date).days
date = start_date
date_str = date.strftime('%Y-%m/%d')
date_str2 = date.strftime('%Y%m%d')
day_count = (end_date - start_date).days
date = start_date
maxpage=8
page=1
page_count=maxpage-page

driver = webdriver.Chrome("./chromedriver")
for i in range(day_count):
    date += dt.timedelta(days=1)
    for page in range(page_count):
        page += 1
        site = 'http://paper.people.com.cn/rmrb/images/'+ str(date.strftime('%Y-%m/%d'))+"/"+str(page).zfill(2)+"/"+"rmrb"+ str(date.strftime('%Y%m%d'))+str(page).zfill(2)+".pdf"
        driver.get(site)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pdf_tags = soup.find_all('pdf')
        filename = str(date)+str(page).zfill(2)
        with open(os.path.join(directory, filename),'wb') as f:
            response = requests.get(site)
            f.write(response.content)
