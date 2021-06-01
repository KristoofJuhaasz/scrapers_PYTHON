import requests
import bs4
import csv
import os
from urllib.request import urlopen
import re
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def crawler(start_page):
    page_list=[]
    page_list.append(start_page)
    for ind in range(len(page_list)+1):
        url=page_list[ind]
        link_list=[]
        link_list=getLinks(url)
        for i in range(len(link_list)):
            page_list.append(link_list[i])
        mail_list=getEmails(url)
        write_to_csv('test.csv', [mail_list])
        #write_to_csv('test_urls.csv', [page_list])
        

        
def write_to_csv(fname, to_be_saved):
    filename = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"], "Desktop", fname)
    myFile = open(filename, 'w', newline='', encoding="utf-8")
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(to_be_saved)    
        
def getLinks(url):
    link_list=[]
    source_code=session.get(url)
    soup = bs4.BeautifulSoup(source_code.text, "lxml")
    for a in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        link_list.append(a['href'])
    return (link_list)

def getEmails(url):
    mail_list=[]
    source_code=session.get(url)
    soup = bs4.BeautifulSoup(source_code.text, "lxml")
    results = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', str(soup))
    for et in results:
        mail_list.append(et)
    return (mail_list)



crawler("http://heller.uni-corvinus.hu/kapcsolat/")