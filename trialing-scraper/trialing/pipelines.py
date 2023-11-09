import sqlite3


class SQLitePipeline(object):
    """
    Part of data pipeline which is used to push data into SQLite. Triggered automatically data yield from spider.
    """
    def __init__(self):
        self.connection = sqlite3.connect('../hospital_data.db')
        self.c = None

    def open_spider(self, spider):
        # Connect to database
        self.c = self.connection.cursor()
        # Create table
        try:
            self.c.execute('''
                CREATE TABLE hospitals (
                    hospital_card_id TEXT,
                    name TEXT,
                    address TEXT,
                    latitude TEXT,
                    longitude TEXT,
                    country TEXT,
                    region TEXT,
                    city TEXT,
                    phone TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass  # Assuming the table already exists.

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # Insert item into database
        self.c.execute('''
            INSERT INTO hospitals (hospital_card_id, name, address, latitude, longitude, country, region, city, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['hospital_card_id'],
            item['name'],
            item['address'],
            item['latitude'],
            item['longitude'],
            item['country'],
            item['region'],
            item['city'],
            item['contact_data']
        ))
        self.connection.commit()
        return item
