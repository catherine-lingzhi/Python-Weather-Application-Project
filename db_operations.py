"""
Description: Final Project Part 2 -Database
Date: 2023-11-09
Usage: Create a DBOperations calss to create datbase using DBCM class.
Group 7: Lingzhi Luo and Alem Bade Bene
"""
from dbcm import DBCM
from scrape_weather import WeatherScraper
from datetime import datetime

class DBOperations:
    def __init__(self, db_name):
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        with DBCM(self.db_name) as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sample_date TEXT UNIQUE,
                    location TEXT,
                    min_temp REAL,
                    max_temp REAL,
                    avg_temp REAL
                )
            ''')

    def purge_data(self):
        with DBCM(self.db_name) as cursor:
            cursor.execute('DELETE FROM weather_data')

    def save_data(self, sample_data):      
        with DBCM(self.db_name) as cursor:
            for date, values in sample_data.items():
                location = "Winipeg"  
                min_temp = values["Min"]
                max_temp = values["Max"]
                avg_temp = values["Mean"]
           
                existing_data = cursor.execute(
                    'SELECT id FROM weather_data WHERE sample_date = ? AND location = ?',
                    (date, location)
                ).fetchone()

                if not existing_data:
                    cursor.execute(
                        'INSERT INTO weather_data (sample_date, location, min_temp, max_temp, avg_temp) '
                        'VALUES (?, ?, ?, ?, ?)',
                        (date, location, min_temp, max_temp, avg_temp)
                    )

    def fetch_data(self):
        with DBCM(self.db_name) as cursor:
            cursor.execute('SELECT * FROM weather_data')
            return cursor.fetchall()

def main():
    current_year = datetime.now().year
    current_month = datetime.now().month 
    myparser = WeatherScraper()
    myparser.scrape_weather_data(current_year, current_month)
    sample_data = myparser.weather_data

    db = DBOperations("weather.sqlite")
    db.save_data(sample_data)
    #db.purge_data()

if __name__=="__main__":
    main()