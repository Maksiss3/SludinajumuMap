import sqlite3
import pandas as pd



class Databases:

    
    def create_db(self, listing):
        city = listing.get('city')
        listing_type = listing.get('listing_type')
        sell_rent = listing.get('sell_rent')
        
        conn = sqlite3.connect(f'databases/{listing_type}/{sell_rent}/{city}.db')
        c = conn.cursor()

        db = pd.json_normalize(listing)
        db.to_sql(city, conn, if_exists='append', index=False)

        conn.commit()
        return db
    
    def read_db(self):
        dat = sqlite3.connect('databases/flats/sell/riga.db')
        query = dat.execute("SELECT * From <TABLENAME>")
        cols = [column[0] for column in query.description]
        return pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
