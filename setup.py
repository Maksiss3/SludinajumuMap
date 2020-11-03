import requests
import re
import sqlite3
import os
from pathlib import Path
from unidecode import unidecode     # To transfer accented text to ascii
from bs4 import BeautifulSoup

from parsers.listing_parser import Parser
from locators.item_locators import Address_fix



current = Path.cwd()


def make_soup(page):
    request = requests.get(page).content
    return BeautifulSoup(request, 'html.parser')

def make_folders(folder_name):
    Path('databases').parent.mkdir(parents=True, exist_ok=True)
    category_path = current / 'databases' / folder_name
    sell_path = current / 'databases' / folder_name / 'izire'
    rent_path = current / 'databases' / folder_name / 'pardod'
    Path(category_path).mkdir(parents=False, exist_ok=True)
    Path(sell_path).mkdir(parents=True, exist_ok=True)
    Path(rent_path).mkdir(parents=True, exist_ok=True)

# for address in ['Iela', 'Bulvāra d. k-1', 'Bebes dambis k-3']:
#     address_words = address.split(' ')
#     for i, word in enumerate(address_words):
#         if word in Address_fix:
#             address_words[i] = Address_fix[word]
#         else:
#             pass
#         address = ' '.join(address_words)
#     print(address)


url = 'https://www.ss.lv/lv/real-estate/flats/riga/centre/'

def get_next_page(url, max_pages = None):
    soup = make_soup(url)
    next_page_tag = soup.select('div.td2 a')
    max_pages_link = next_page_tag[0]['href'].split('/')
    max_pages_withhtml = max_pages_link[-1].strip('page')
    max_pages = max_pages_withhtml.strip('.html')
    print(max_pages)

    if max_pages == None:
        max_pages = 50

    for i in range(1,3):
        next_page_href = next_page_tag[-1]['href']
        next_page = f'{url}{next_page_href}'
        print(next_page)