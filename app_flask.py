import folium
from flask import Flask, render_template

from locators.geo_map import Geolocation
from databases.database_control import Databases
app = Flask(__name__)

listing2 = {
            'href' : 'https://www.ss.lv/lv/msg/lv/real-estate/flats/riga/centre/ajiep.html',
            'thumbnail' : 'https://i.ss.lv/gallery/4/712/177959/35591764.th2.jpg',
            'address' : 'Dzirnavu 51',
            'listing_type': 'flats',
            'city': 'riga',
            'region': 'centre',
            'm2' : 90,
            'rooms' : 4,
            'price' : 149500,
            'price_per_m2' : 1661,
            'sell_rent': 'sell',
            'latitude' : 56.9568138,
            'longitude' : 24.1172697,
            }

# geo = Geolocation(listing2)
# geo.create_map

# db_class = Databases()
# db = db_class.read_db
# print(db.longitude)


@app.route('/')
def index():
    # geo = Geolocation(listing2)
    # geo.create_map
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True)