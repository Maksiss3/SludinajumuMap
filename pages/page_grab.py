
from bs4 import BeautifulSoup

from locators.item_locators import TAG_LOCATORS
from setup import make_soup
locators = TAG_LOCATORS


class URLs:
    """
    Creates ready-to-scrape listing URLs. Input = [soup, listing category link (house,apartment,truck)]
    """
    def __init__(self, link):
        self.link = link                                                      # link of the main category page (ex: 'https://www.ss.lv/lv/real-estate/flats/')


    def get_subcateg_links(self, soup):                                       # Input a soup of the region choice page
        name_locator = locators.REGION_NAME_LOCATOR

        subcateg = soup.select(name_locator)                                  # Select sub tags
        subcateg_li = [sub.text for sub in subcateg]                          # Make a list of readable sub names
        all_links = [sub['href'] for sub in subcateg]

        URL_list = [i.split("/") for i in all_links]                          # .split() the link phrases
        URL_list = ["/".join(x[-2:]) for x in URL_list]
        dictionary =  dict(zip(subcateg_li, URL_list))
        dictionary.pop('Visi sludinājumi', None)                              # Remove 'all' category from dictionary

        return dictionary                                                     # Get a dictionary of cities and its URL values


    def make_url(self, soup):
        cities_with_regions = ['riga','daugavpils','liepaja']                 # Specifying cities that have extra regions
        urls = []
        subcateg = self.get_subcateg_links(soup)                              # Get all cities and their URL values
        for sub, url in subcateg.items():
            if any(city in url for city in cities_with_regions):              # If any of those urls contain previously specified cities with regions, go trough those regions first
                region_soup = make_soup(self.link + url)
                region_urls = self.make_url_regions(region_soup,url)
                urls.append(region_urls)
            else:
                for x in ['sell/','hand_over/']:
                    urls.append(self.link + url + x)
        return urls

    def make_url_regions(self,soup,city):
        urls=[]
        subcateg_region = self.get_subcateg_links(soup)
        for sub, url in subcateg_region.items():
            for x in ['sell/','hand_over/']:
                urls.append(self.link + city + url + x)
        return urls

    
    def city_from_url(self, url):
        URL_list =url.split("/")                                # .split() the link phrases
        del URL_list[-2]                                        # Delete the sell / hand_over part
        if URL_list[7]:                                         # Check if the URL has a region value
            region = URL_list[7] 
        else:
            region = None
        return URL_list[5], URL_list[6], region


    def get_max_pages(self, url):
        soup = make_soup(url)
        next_page_tag = soup.select('div.td2 a')
        max_pages_link = next_page_tag[0]['href'].split('/')
        max_pages_clutter = max_pages_link[-1].strip('page')
        return int(max_pages_clutter.strip('.html'))

    def get_next_page(self, url, max_pages):
        soup = make_soup(url)
        next_page_tag = soup.select('div.td2 a')
        next_page_href = next_page_tag[-1]['href']
        next_url = f'{url}{next_page_href}'
        return next_url



