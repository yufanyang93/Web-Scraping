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
from selenium.common.exceptions import NoSuchElementException

path = "/Volumes/Mac/Historical Newspaper"
os.chdir(path)

start_date = dt.date(1946, 5, 1)
end_date = dt.date(2003, 12, 31)
day_count = (end_date-start_date).days
date = start_date
date_str = date.strftime('%Y-%m-%d')
day_count = (end_date - start_date).days
date = start_date
directory = os.getcwd()

driver = webdriver.Chrome("./chromedriver")
for i in range(day_count):
    date += dt.timedelta(days=1)
    for page in range(0, 4):
        page += 1
        try:
            site = 'https://www.laoziliao.net/rmrb/'+ str(date.strftime('%Y-%m-%d'))+"-"+str(page).zfill(2)
            driver.get(site)
            elements = driver.find_elements_by_class_name("article")
            for element in elements:
                filename = str(date)+str(page).zfill(2)+str(element.id)
                with open(os.path.join(directory, filename+".txt"),'w') as f:
                    f.write(element.text)
        except NoSuchElementException:
            pass
