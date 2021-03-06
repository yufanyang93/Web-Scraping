import os
import glob
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import requests

dir = "/Volumes/Mac/RU/data"
os.chdir(dir)

url = "https://rg.ru/"
driver = webdriver.Chrome('./chromedriver')
driver.get(url)

linklist = []
def get_link(i, j):
    for i in range(113):
        trigger = driver.find_element_by_xpath('//*[@id="datePanel"]/div/div/div[4]/div/div/button')
        ActionChains(driver).click(trigger).perform()
        hidden_button = driver.find_element_by_class_name('pika-prev')
        ActionChains(driver).click(hidden_button).perform()
        trigger = driver.find_element_by_xpath('//*[@id="datePanel"]/div/div/div[4]/div/div/button')
        ActionChains(driver).click(trigger).perform()
        list_days = driver.find_elements_by_css_selector("button.pika-button.pika-day")
        count = len(list_days)

        j = 1
        for j in range(count):
            trigger = driver.find_element_by_xpath('//*[@id="datePanel"]/div/div/div[4]/div/div/button')
            ActionChains(driver).click(trigger).perform()
            date_button = driver.find_elements_by_css_selector('button.pika-button.pika-day')[j]
            ActionChains(driver).click(date_button).perform()
            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            links = soup.find_all('h2', attrs = {'class': 'b-news__list-item-title'})

            for link in links:
                url = link.a['href']
                linklist.append(url)
            j+=1

        i+=1
    return linklist

def fetchUrl(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    r = requests.get(url,headers=headers)
    if r.status_code!=200:
        pass
    r.encoding = r.apparent_encoding
    return r.text

ru_date = []
ru_title = []
ru_content = []

for link in linklist:
    url = 'https://rg.ru' + link
    html = fetchUrl(url)
    bsobj = BeautifulSoup(html, 'html.parser')
    title = bsobj.find('h1', attrs = {'class': 'b-material-head__title'})
    if title is None:
        title = bsobj.find('h1', attrs = {'class': 'b-material-wrapper__title'})
        if title is None:
            title = bsobj.find('div', attrs = {'class': 'b-material-head__title'})

    if title is not None:
        title_text = title.text

    date = bsobj.find('span', attrs = {'class': 'b-material-head__date-day'})
    if date is None:
        date = bsobj.find('span', attrs = {'class': 'b-material-date__day'})
        if date is None:
            date = bsobj.find('div', attrs = {'class': 'b-material-head__date-item b-material-head__date-day'})

    if date is not None:
        date_text = date.text

    content_list = bsobj.find('div', attrs = {'class': 'b-material-wrapper__text'})
    if content_list is None:
        content_list = bsobj.find('article', attrs = {'class': 'b-material-wrapper__body'})

    if content_list is not None:
        content_list = content_list.find_all('p')

        content = ''
        for p in content_list:
            content += p.text + '\n'
            if content is None:
                continue

    ru_date.append(date_text)
    ru_title.append(title_text)
    ru_content.append(content)   

ru_df =pd.DataFrame(list(zip(ru_date, ru_title, ru_content)), columns = ['date', 'title', 'content'])
