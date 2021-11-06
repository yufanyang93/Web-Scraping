import re
import requests
from bs4 import BeautifulSoup
import os
import datetime
import pandas as pd
import urllib.request
from selenium import webdriver
from uuid import uuid4

#Web scraping@
driver = webdriver.Chrome("./chromedriver")

start_year = 2013
end_year = 2021

year_count = end_year - start_year
year = start_year
folder_location="./pravda"
response = requests.get(url)

j=1

for i in range(year_count):
    year += 1
    for j in range(4):
        j += 1
        url ='https://gazeta-pravda.ru/issue/archive/year/' + str(year) +'/?PAGEN_2='+str(j)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for link in soup.select("a[href$='.pdf']"):
            filename = os.path.join(folder_location,link['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url,link['href'])).content)

#Extract Content from pdf to txt file#
#First extract metadata$
import glob
import tika
tika.initVM()
from tika import parser
from PyPDF2 import PdfFileReader
import csv
from tika import translate

def extractor():
    basedir = os.getcwd()
    extension = '*.pdf'
    pdffiles = glob.glob(os.path.join(basedir, "Pravda", extension))

    with open('pdfmetadata.csv', 'w') as csvfile:
        for f in pdffiles:
                pdf_to_read = parser.from_file(f)
                pdf_info = pdf_to_read["metadata"]
                title = pdf_info['title']
                date = pdf_info['Creation-Date']
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([title, date])

if __name__ == "__main__":
        extractor()

#Then extract text#
from io import StringIO
import codecs
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from googletrans import Translator

output_string = StringIO()

def extract_content():
    basedir = os.getcwd()
    extension = '*.pdf'
    pdffiles = glob.glob(os.path.join(basedir, extension))
    translator = Translator()

    for pdffile in pdffiles:
        with open(pdffile, 'rb') as in_file:
                parser = PDFParser(in_file)
                doc = PDFDocument(parser)
                rsrcmgr = PDFResourceManager()
                device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.create_pages(doc):
                    interpreter.process_page(page)

                text = output_string.getvalue()
                text = re.sub('\r', '\n', text)
                text = re.sub('\(cid\:(\d+)\)', '', text)

        with open((pdffile.rsplit('.', 1)[0]) + '.txt', 'w') as f:
                f.write(text + '\n')

extract_content()

###check and delete duplicate files##
import sys
import os
import hashlib

check_path = (lambda filepath, hashes, p = sys.stdout.write:
        (lambda hash = hashlib.sha1 (file (filepath).read ()).hexdigest ():
                ((hash in hashes) and (p ('DUPLICATE FILE\n'
                                          '   %s\n'
                                          'of %s\n' % (filepath, hashes[hash])))
                 or hashes.setdefault (hash, filepath)))())

scan = (lambda dirpath, hashes = {}:
                map (lambda (root, dirs, files):
                        map (lambda filename: check_path (os.path.join (root, filename), hashes), files), os.walk (dirpath)))

((len (sys.argv) > 1) and scan (sys.argv[1]))
