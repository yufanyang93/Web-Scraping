import os
import glob
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
import time

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

