import requests
import re

from locators.item_locators import TAG_LOCATORS, Address_fix


class Parser:
    """
    A class to take in an HTML page or content, and find properties of an item
    in it.
    """

    def __init__(self, soup, listing):
        self.soup = soup
        self.listing = listing

    @property
    def get_href(self):
        href = self.listing[0].find("a").get("href")
        return 'https://www.ss.lv/lv' + href

    @property
    def get_address(self):
        address = self.listing[2].text
        address_words = address.split(' ')                                          # Split address into a list of words (Sometimes addresses are incomplete / have values that can't be turned into coordinates)
        for i, word in enumerate(address_words):                                    # Go trough that list
            if word in Address_fix:
                address_words[i] = Address_fix[word]                                # If a known address issue is found, change it to the correct value from Address_fix dictionary
            else:
                pass
        return ' '.join(address_words)                                              # Turn the words back into an address string

    @property
    def get_thumbnail(self):
        return self.listing[0].find('a').find('img').attrs['src']

    @property
    def get_rooms(self):
        return self.listing[3].text

    @property
    def get_m2(self):
        return self.listing[4].text

    @property
    def get_price(self):
        return self.listing[8].text

    @property
    def get_price_per_m2(self):
        return self.listing[7].text


        
            