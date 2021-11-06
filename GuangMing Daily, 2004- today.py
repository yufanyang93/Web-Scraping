import requests
import bs4
import os
import datetime
import time

dir = "/Volumes/Mac/GuangMing"
os.chdir(dir)

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

def getPageList(year, month, day):
    url = 'https://www.gmw.cn/01gmrb/' + year + '-' + month + '/' + day + '/' + year + '-' + month + '-' + day + '-' + 'Homepage.htm'
    html = fetchUrl(url)
    if len(html)!=4114:
        bsobj = bs4.BeautifulSoup(html,'html.parser')
        pageList = bsobj.find('div', attrs = {'class': 'channelLeftPart'}).find_all('ul', attrs = {'class': 'channel-newsGroup'})
        linkList = []

        for page in pageList:
            links = page.find_all('span', attrs = {'class': 'channel-newsTitle'})
            for link in links:
                try:
                    id = link.a['href']
                    url = 'https://www.gmw.cn/01gmrb/' + year + '-' + month + '/' + day + '/' + id
                    linkList.append(url)
                except link.HTTPError as e:
                    if e.getcode() == 404:
                        continue
                    raise
        return linkList

    else:
        print ("no content")
        pass

def getContent(html):
    if len(html)!=4114:
        bsobj = bs4.BeautifulSoup(html,'html.parser')
        title = bsobj.h1.text
        pList = bsobj.find('div', attrs = {'id': 'contentMain'}).find_all('p')
        content = ''
        for p in pList:
            content += p.text + '\n'
            if content is None:
                continue
        resp = title + content
        return resp
    else:
        print ("no content")
        pass

def saveFile(content, path, filename):

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)

def download_gmrb(year, month, day, destdir):
    pageList = getPageList(year, month, day)
    if pageList != None:
        for url in pageList:
            html = fetchUrl(url)
            content = getContent(html)
            if content is None:
                continue

            temp = url.split('/')
            titleNo = temp[6]
            path = destdir + '/' + year + month + day + '/'
            fileName = year + month + day + '-' + titleNo + '.txt'

            saveFile(content, path, fileName)
    else:
        print("no content")
        pass

def gen_dates(b_date, days):
    day = datetime.timedelta(days = 1)
    for i in range(days):
        yield b_date + day * i

def get_date_list(beginDate, endDate):

    start = datetime.datetime.strptime(beginDate, "%Y%m%d")
    end = datetime.datetime.strptime(endDate, "%Y%m%d")

    data = []
    for d in gen_dates(start, (end-start).days):
        data.append(d)

    return data

if __name__ == '__main__':
    beginDate = input('Start Date (yyyy/mm/dd):')
    endDate = input('End Date (yyyy/mm/dd):')
    data = get_date_list(beginDate, endDate)

    for d in data:
        year = str(d.year)
        month = str(d.month) if d.month >=10 else '0' + str(d.month)
        day = str(d.day) if d.day >=10 else '0' + str(d.day)
        download_gmrb(year, month, day, 'data')
        print("Done：" + year + month + day)

##From 2004-03-01 to 2008-01-01
##Simply change the URL to: https://www.gmw.cn/01gmrb/2004-03/01/default.htm

##From 2008-01-02
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

def getPageList(year, month, day):
    url = 'https://epaper.gmw.cn/gmrb/html/' + year + '-' + month + '/' + day + '/nbs.D110000gmrb_01.htm'
    html = fetchUrl(url)

    if len(html)!=1203 & len(html)!=0:
        bsobj = bs4.BeautifulSoup(html,'html.parser')
        pageList = bsobj.find('div', attrs = {'id': 'pageList'}).ul.find_all('a', attrs = {'id': 'pageLink'})
        linkList = []

        for page in pageList:
            link = page.get("href")
            url = 'https://epaper.gmw.cn/gmrb/html/' + year + '-' + month + '/' + day + '/' + link
            linkList.append(url)
        return linkList

    else:
        print ("no content")
        pass

def getTitleList(year, month, day, pageUrl):
    html = fetchUrl(pageUrl)
    if len(html)!=1203 & len(html)!=0:
        bsobj = bs4.BeautifulSoup(html,'html.parser')
        titleList = bsobj.find('div', attrs = {'id': 'titleList'}).ul.find_all('li')
        linkList = []

        for title in titleList:
            tempList = title.find_all('a')
            for temp in tempList:
                link = temp["href"]
                if 'nw.D110000gmrb' in link:
                    url = 'https://epaper.gmw.cn/gmrb/html/'  + year + '-' + month + '/' + day + '/' + link
                    linkList.append(url)

        return linkList

    else:
        print ("no content")
        pass

def getContent(html):
    if len(html)!=1203 & len(html)!=0:
        bsobj = bs4.BeautifulSoup(html,'html.parser')
        title = bsobj.h1.text
        pList = bsobj.find('div', attrs = {'id': 'articleContent'}).find_all('p')
        content = ''
        for p in pList:
            content += p.text + '\n'
            if content is None:
                continue
        resp = title + content
        return resp
    else:
        print ("no content")
        pass

def saveFile(content, path, filename):

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)

def download_gmrb(year, month, day, destdir):
    pageList = getPageList(year, month, day)
    if pageList is not None:
        for page in pageList:
            titleList = getTitleList(year, month, day, page)
            if titleList is not None:

                for url in titleList:
                    html = fetchUrl(url)
                    content = getContent(html)
                    if content is None:
                        continue

                    temp = url.split('/')
                    titleNo = temp[7]
                    path = destdir + '/' + year + month + day + '/'
                    fileName = year + month + day + '-' + titleNo + '.txt'

                    saveFile(content, path, fileName)
            else:
                print("no content")
                pass
    else:
        print("no content")
        pass

def gen_dates(b_date, days):
    day = datetime.timedelta(days = 1)
    for i in range(days):
        yield b_date + day * i

def get_date_list(beginDate, endDate):

    start = datetime.datetime.strptime(beginDate, "%Y%m%d")
    end = datetime.datetime.strptime(endDate, "%Y%m%d")

    data = []
    for d in gen_dates(start, (end-start).days):
        data.append(d)

    return data

if __name__ == '__main__':
    beginDate = input('Start Date (yyyy/mm/dd):')
    endDate = input('End Date (yyyy/mm/dd):')
    data = get_date_list(beginDate, endDate)

    for d in data:
        year = str(d.year)
        month = str(d.month) if d.month >=10 else '0' + str(d.month)
        day = str(d.day) if d.day >=10 else '0' + str(d.day)
        download_gmrb(year, month, day, 'data')
        print("Done：" + year + month + day)
