import urllib.request
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from os import listdir
from os.path import isfile, join
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

mypath = 'data/images'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles = [f.replace('.jpg', '') for f in onlyfiles]
print(onlyfiles)

df = pd.read_csv('data/all_recipes/item-profiles2.csv',  on_bad_lines='skip', sep = ';')
def scrape(id, name):

    def getsoup(url):
        req = requests.get(url)
        html = None
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
            return soup
        else:
            print('FAILED')
            return 0

    def storeimage(id, url):
        file_name = f'data/images/{id}.jpg' #prompt user for file_name
        sleeptime = random.uniform(0.2,0.5)
        print(id, url)
        try:
            urllib.request.urlretrieve(url, file_name)
            print(f'{bcolors.HEADER}\nCrawled for {id} next in {sleeptime:.3f} seconds.{bcolors.ENDC}')
        except Exception as e:
            print(e)
            print(f'{bcolors.FAIL}\nCrawled failed for {id} next in {sleeptime:.3f} seconds.{bcolors.ENDC}')
        time.sleep(sleeptime)
            
        return 1

    # 'https://www.allrecipes.com/search?q=broccoli+beef+I'
    # 'https://www.allrecipes.com/search?q=asdf'
    name = name.replace(' ', '+')
    first_item_id = 'mntl-card-list-items_1-0'
    url = f'https://www.allrecipes.com/search?q={name}'

    soup = getsoup(url)
    if soup:
        first_item = soup.find(id=first_item_id)
        try:
            article_link = first_item['href']
        except Exception as e:
            print(f'{bcolors.FAIL}\nFailed for item {first_item}{bcolors.ENDC}', e)
            return 0
        try:
            soup = getsoup(article_link)
            if soup:
                image = soup.select('.primary-image__image')
                if not image:
                    image = soup.select('#mntl-sc-block-image_1-0-1')
                if image:
                    for elem in image:
                        if 'loaded' in elem['class']:
                            storeimage(id, elem['src'])
                        return 1
                else:
                    print('image not found for image ID: ')
            css_selector = '.primary-image__image'
            xpath = '//*[@id="mntl-sc-block-image_1-0-1"]'
        except Exception as e:
            print(f'{bcolors.FAIL}\nSomething went wrong :({bcolors.ENDC}', e)

def rowapply():
    return

for row in df.itertuples():
    if str(row._1) not in onlyfiles:
        print(f'{bcolors.OKGREEN}\nScraping{bcolors.ENDC}', row._1, row.Name)
        scrape(row._1, row.Name)
    else:
        print(row._1, row.Name, ' Already scraped.')