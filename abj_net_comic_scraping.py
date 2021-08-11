# Program skeleton #
####################
"""
Overview

Program skeleton

How to run this Program?

Sample output
"""
import os, sys, random, time
import requests
import datetime
import threading
from bs4 import BeautifulSoup


# 82984150

"""
url = "https://news.abidjan.net/caricatures"
yr = 2021
mth = 8


def get_dates(dt_string):
    pass

class Crawler:
    def __init__(self, url, start_date, end_date):
        pass
    def run(self):
        pass
    def get_responses(self):
        pass
    def write(self, content):
        pass
"""

class Crawler:
    def __init__(self, url, year, month, N_threads):
        self.url = url
        self.year = year
        self.month = month
        self.nthreads = N_threads

    def get_images(self, url):
        img_urls = []
        res = requests.get(page_url, allow_redirects=False, stream = True)
        soup = BeautifulSoup(res.content, features="lxml")
        for tag in soup.findAll('img'):
            if not 'img' in tag.get('src'):
                continue
            img_url = tag.get('data-original')
            if img_url:
                img_urls.append(img_url)
        img_urls = set(img_urls)
        self.download_images(img_urls)

    def download_images(self, img_list):
        if img_list:
            path = 'year%s/month%s' %(self.year,self.month)
            os.makedirs(path, exist_ok = True)
            self.write_images(path,img_list)

    def write_images(self, img_path, img_container):
        for link in img_container:
            with open(os.path.join(img_path, os.path.basename(link)),'wb') as w_handl:
                try:
                    img_resp = requests.get(link)
                except:
                    continue        
                for chunk in img_resp.iter_content(1024):
                    w_handl.write(chunk)

    def run(self):
        for i in range(eval(self.nthreads)):
            t = threading.Thread(target=self.get_images, args = (self.url,))
            t.start()
            time.sleep(random.randint(1,5))


if __name__ == '__main__':

    page_url = "https://news.abidjan.net/caricatures"
    yr, mo, N = sys.argv[1], sys.argv[2], sys.argv[3] 
    crawler = Crawler(page_url, yr, mo, N)
    crawler.run()
