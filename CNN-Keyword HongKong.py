import os
path="/HongKong"
os.chdir(path)

##Using selenium get CNN
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

path = "/Volumes/Mac/HongKong/CNN"
os.chdir(path)

driver = webdriver.Chrome("./chromedriver")

##Get Page 1##
base_url = 'https://edition.cnn.com/search?size=10&q=Hong%20Kong&page=1'
driver.get(base_url)
time.sleep(1)

main_news_container = driver.find_element_by_class_name('cnn-search__results-list')
text_sections = main_news_container.find_elements_by_xpath("//a[@href]")

pos = 0
df = pd.DataFrame(columns = ['date', 'headline', 'content'])

for ele in main_news_container.find_elements_by_class_name('cnn-search__result-contents'):
    data = []
    publish_date = ele.find_element_by_class_name('cnn-search__result-publish-date').text
    headline = ele.find_element_by_class_name('cnn-search__result-headline').text
    content = ele.find_element_by_class_name("cnn-search__result-body").text
    data.append(publish_date)
    data.append(headline)
    data.append(content)
    df.loc[pos] = data
    pos+=1


cnn_date = []
cnn_title = []
cnn_content = []
cnn_df = pd.DataFrame(columns = ['date', 'headline', 'content'])
def cnn_scraper (j):
    i = []

    for j in range(2, 500):
        i = 10*(j-1)
        base_url = 'https://edition.cnn.com/search?q=Hong%20Kong&size=10&from=' + str(i) + '&page=' + str(j)
        driver.get(base_url)
        time.sleep(1)
        main_news_container = driver.find_element_by_class_name('cnn-search__results-list')

        pos = 0
        df_temp = pd.DataFrame(columns = ['date', 'headline', 'content'])
        for ele in main_news_container.find_elements_by_class_name('cnn-search__result-contents'):
            data = []
            publish_date = ele.find_element_by_class_name('cnn-search__result-publish-date').text
            headline = ele.find_element_by_class_name('cnn-search__result-headline').text
            content = ele.find_element_by_class_name("cnn-search__result-body").text
            data.append(publish_date)
            data.append(headline)
            data.append(content)
            df_temp.loc[pos] = data
            pos+=1

        cnn_date.append(df_temp['date'])
        cnn_title.append(df_temp['headline'])
        cnn_content.append(df_temp['content'])
        j+=1
    return cnn_df

cnn_scraper(2)

cnn_date = pd.concat(cnn_date)
cnn_title = pd.concat(cnn_title)
cnn_content = pd.concat(cnn_content)

cnn_date = cnn_date.to_frame()
cnn_title = cnn_title.to_frame()
cnn_content = cnn_content.to_frame()

cnn_date.index = range(4850)
cnn_title.index = range(4850)
cnn_content.index = range(4850)

cnn_df = cnn_date.merge(cnn_title, left_index = True, right_index = True)
cnn_df = cnn_df.merge(cnn_content, left_index = True, right_index = True)
