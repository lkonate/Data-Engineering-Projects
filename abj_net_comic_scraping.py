import os
os.chdir('C:\\Users\\lamine konate\\Documents')

import requests
from bs4 import BeautifulSoup

url='http://news.abidjan.net/caricatures/'

os.makedirs('gbich', exist_ok=True)
res=request.get(url)
res.raise_for_status()
soup=BeautifulSoup(res.text)
comicElem=soup.select('#a href img')
if comicElem==[]:
	print('Could not find comic img')
else:
	try:
		comicurl=comicElem[1].get(src)
		print('Downloading image %s...' %(comicurl)
		res=requests.get(comicurl)
		res.raise_for_status()
	except requests.exceptions.MissingSchema:
		ImageFile=open(os.path.join('gbich',os.path.basename(comicurl)),'wb')
		for chunk in res.iter_content(100000)
			imageFile.write(chunk)
		imageFile.close()

#############################################################################


import csv
import requests
from bs4 import BeautifulSoup

url = 'news.abidjan.net/caricatures/'
res = requests.get(url)
res.raise_for_status()
html = res.content

soup = BeautifulSoup(html)
table = soup.find('tbody', attrs={'class': 'stripe'})

list_of_rows = []
for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll('td'):
        list_of_cells.append(cell)
    list_of_rows.append(list_of_cells)

outfile = open("./inmates.csv", "wb")

#############################################################################

import os
os.chdir('C:\\Users\\lamine konate\\Documents')

import requests
from bs4 import BeautifulSoup

url='http://news.abidjan.net/caricatures/'

for o in range(2005,2017):
	for p in range(1,13):
		for q in range(1,32):
			url='http://news.abidjan.net/caricatures/archives.asp?d=%s/%s/%s&j=%s&m=%s&a=%s'%(q,p,o,q,p,o)

os.makedirs('gbich', exist_ok=True)
res=requests.get(url)
res.raise_for_status()
soup=BeautifulSoup(res.text)
table = soup.find('div', attrs={'id': 'main'})
list_of_rows = []
for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll('td'):
        list_of_cells.append(cell)
    list_of_rows.append(list_of_cells)

comicElem=soup.select('img')
if comicElem==[]:
	print('Could not find comic img')
else:
	try:
		comicurl=comicElem[-1].get('src')
		print('Downloading image %s...' %(comicurl)
		res=requests.get(comicurl)
		res.raise_for_status()
	except requests.exceptions.MissingSchema:
		ImageFile=open(os.path.join('gbich',os.path.basename(comicurl)),'wb')
		for chunk in res.iter_content(100000)
			imageFile.write(chunk)
		imageFile.close()
#############################################################################

import os, random, time
import requests
from bs4 import BeautifulSoup

for o in range(2012,2017):
	for p in range(1,13):
		for q in range(1,32):
			url='http://news.abidjan.net/caricatures/archives.asp?d=%s/%s/%s&j=%s&m=%s&a=%s'%(q,p,o,q,p,o)
			url_hc=url
			html=requests.get(url_hc, allow_redirects=False)
			time.sleep(random.randrange(5))
			if html.status_code!=200:
				print('No comic on: %s/%s/%s' %(q,p,o))
			else:
				soup= BeautifulSoup(html.text)
				tags= soup('img')
				for tag in tags:
					if 'img' in tag.get('src'):
						img_url= tag.get('src')
						html2= requests.get(img_url)
						path='year%s/month%s' %(o,p)
						os.makedirs(path, exist_ok=True)
						with open(os.path.join(path, os.path.basename(img_url)[5:]),'wb') as image:
							for chunk in html2.iter_content(100000):
								image.write(chunk)

###########################################################################

Project: Scraping webpages on Comics and Storing data in Folders


import os
os.chdir('C:\\Users\\lamine konate\\Documents')

import requests
from bs4 import BeautifulSoup

url='http://news.abidjan.net/caricatures/'

for o in range(2005,2017):
	for p in range(1,13):
		for q in range(1,32):
			url='http://news.abidjan.net/caricatures/archives.asp?d=%s/%s/%s&j=%s&m=%s&a=%s'%(q,p,o,q,p,o)

os.makedirs('gbich', exist_ok=True)
res=requests.get(url)
res.raise_for_status()
soup=BeautifulSoup(res.text)
table = soup.find('div', attrs={'id': 'main'})
list_of_rows = []
for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll('td'):
        list_of_cells.append(cell)
    list_of_rows.append(list_of_cells)

comicElem=soup.select('img')
if comicElem==[]:
	print('Could not find comic img')
else:
	try:
		comicurl=comicElem[-1].get('src')
		print('Downloading image %s...' %(comicurl)
		res=requests.get(comicurl)
		res.raise_for_status()
	except requests.exceptions.MissingSchema:
		ImageFile=open(os.path.join('gbich',os.path.basename(comicurl)),'wb')
		for chunk in res.iter_content(100000)
			imageFile.write(chunk)
		imageFile.close()

-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0-0+0+0

(Same as above)

import os, random, time
import requests
from bs4 import BeautifulSoup

for o in range(2012,2017):
	for p in range(1,13):
		for q in range(1,32):
			url='http://news.abidjan.net/caricatures/archives.asp?d=%s/%s/%s&j=%s&m=%s&a=%s'%(q,p,o,q,p,o)
			url_hc=url
			html=requests.get(url_hc, allow_redirects=False)
			time.sleep(random.randrange(5))
			if html.status_code!=200:
				print('No comic on: %s/%s/%s' %(q,p,o))
			else:
				soup= BeautifulSoup(html.text)
				tags= soup('img')
				for tag in tags:
					if 'img' in tag.get('src'):
						img_url= tag.get('src')
						html2= requests.get(img_url)
						path='year%s/month%s' %(o,p)
						os.makedirs(path, exist_ok=True)
						with open(os.path.join(path, os.path.basename(img_url)[5:]),'wb') as image:
							for chunk in html2.iter_content(100000):
								image.write(chunk)


def custom_day_scraper(y_start=2018,y_end=2020,m_start=1,m_end=12,d_start=1,d_end=31 ): 
    for o in range(y_start,y_end+1): 
        for p in range(m_start,m_end+1): 
            for q in range(d_start,d_end+1): 
                url='https://news.abidjan.net/caricatures/archives.asp?d=%s/%s/%s&j=%s&m=%s&a=%s'%(q,p,o,q,p,o) 
                url_hc=url 
                html=requests.get(url_hc, allow_redirects=False) 
                time.sleep(random.randrange(5)) 
                if html.status_code!=200: 
                    print('No comic on: %s/%s/%s' %(p,q,o)) 
                else: 
                    soup= BeautifulSoup(html.text) 
                    tags= soup('img') 
                    for tag in tags: 
                        if 'img' in tag.get('src'): 
                            img_url= tag.get('src') 
                            html2= requests.get(img_url) 
                            path='year%s/month%s' %(o,p) 
                            os.makedirs(path, exist_ok=True) 
                            with open(os.path.join(path, os.path.basename(img_url)[5:]),'wb') as imag: 
                                for chunk in html2.iter_content(100000): 
                                    imag.write(chunk)
