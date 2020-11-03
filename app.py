import time
import logging
import pandas as pd
from bs4 import BeautifulSoup

from setup import make_soup
from databases.database_control import Databases
from pages.page_grab import URLs
from locators.item_locators import Webpages, Address_fix
from locators.geo_map import Geolocation, Map
from parsers.listing_parser import Parser


logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('scraping')


web = dict(vars(Webpages))                                                      # Get a list of variables from the class Webpages
for junk in ['__module__','__dict__','__weakref__','__doc__']:                  # Remove unneeded values from list
    if junk in web: del web[junk]


for page, web_address in web.items():                                               # Go trough all the web addresses (of categories) in item_locators.Webpages
    x = URLs(web_address)                                                           # Initates the URLs class
    urls_list = x.make_url(make_soup(web_address))                                  # Creates a list of URLs from the given address and it's soup   
    urls = []

    for z in urls_list:                                                             #Create a usable list of URLs
        if isinstance(z, list):
            for y in z:
                urls.append(y)
        else:
            urls.append(z)

    for url in urls:
        logger.info(f'Starting URL: {url}')

        max_pages = x.get_max_pages(url)
        if max_pages > 25:
            max_pages = 25

        next_url = url
        while next_url:                                                                 # Goes trough the parsing pages while there are pages to go trough (or set a limit in the appropriate function)
            soup = make_soup(next_url)
            listing_type, city, region = x.city_from_url(url)
            
            for all_listings in soup.find_all('tr')[5:-4]:                              # Creates a list of all listings seperately, for example [1.st value = 1.st apartment listing and it's descriptions], And everything before [5:] is unneded other website tables
                try:
                    listing_li = all_listings.find_all('td')[1:]                        # Creates a list all the description values in the specified listing [description, rooms, price, m2, ...]
                    parser = Parser(soup, listing_li)                                         

                    listing = {
                        'href' : parser.get_href,
                        'thumbnail' : parser.get_thumbnail,
                        'address' : parser.get_address,
                        'listing_type': listing_type,
                        'city': city,
                        'region': region,
                        'm2' : parser.get_m2,
                        'rooms' : parser.get_rooms
                    }
                    
                    geo = Geolocation(listing)                                          
                    latitude, longitude = geo.get_coordinates                           # Creates coordinates from 'city' and 'address' values

                    price = parser.get_price.strip('  €').replace(',', '')                  # Create simpler price values for database
                    price_per_m2 = parser.get_price_per_m2.strip('  €').replace(',', '')

                    listing.update({'price' : price})
                    listing.update({'price_per_m2' : price_per_m2})
                    listing.update({'sell_rent': 'sell'}) if '/sell/' in url else listing.update({'sell_rent':'rent'})
                    listing.update({'latitude' : latitude})
                    listing.update({'longitude' : longitude})
                    
                    db_class = Databases()
                    print(db_class.create_db(listing))
                    # time.sleep(1)

                except IndexError:
                    print('Something went wrong')
                    pass

            next_url = x.get_next_page(url, max_pages)
            logger.info(f'Listings scraped, going to next page: {next_url}')
