import folium
import sqlite3
import pandas as pd
from geopy.geocoders import Nominatim

class Geolocation:

    def __init__(self, listing):
        self.listing = listing
    
    @property
    def get_coordinates(self):
        try:
            nom = Nominatim(user_agent="maksiss_sludinajumi")
            address = self.listing.get('address')
            city = self.listing.get('city')
            n = nom.geocode(f'{address}, {city}')
            return n.latitude, n.longitude
        except:
            print("Couldn't get coordinates from address")  # Change to logger later
            return None, None



class Map:

    def __init__(self, db):
        self.db = db

    @property
    def create_map(self):
        map_lv = folium.Map(location = [56.96,24.12], tiles='openstreetmap', zoom_start = 7)
        map_lv.save('templates/map.html')
        return map_lv

    # @property
    # def listing_to_map(self):
        
    #     for idx, row in self
    #     self.map_lv

