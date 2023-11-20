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
    """Class for performing operations on a weather data SQLite database."""   
    def __init__(self, db_name):
        """Initializes the DBOperations instance with the specified database name."""
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        """Creates the 'weather_data' table if it doesn't exist in the database."""
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
        """Deletes all data from the 'weather_data' table."""
        with DBCM(self.db_name) as cursor:
            cursor.execute('DELETE FROM weather_data')

    def save_data(self, sample_data):
        """ Saves weather data to the 'weather_data' table."""
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
        """Retrieves data from the 'weather_data' table for creating plots"""
        with DBCM(self.db_name) as cursor:
            cursor.execute('SELECT sample_date, avg_temp FROM weather_data')
            data_from_db = cursor.fetchall()

        plotter_data = {}
        for row in data_from_db:
            date, avg_temp = row  

            try:              
                dt = datetime.strptime(date, "%Y-%m-%d")

                year = dt.year
                month = dt.month

                if year not in plotter_data:
                    plotter_data[year] = {}

                if month not in plotter_data[year]:
                    plotter_data[year][month] = {}

                day = dt.day
                plotter_data[year][month][day] = avg_temp

            except ValueError as e:
                print(f"Error: Unable to parse date {date}. {e}")
                continue

        return plotter_data

def main():
    # Save scrapping data to the database    
    current_year = datetime.now().year
    current_month = datetime.now().month 
    myparser = WeatherScraper()
    myparser.scrape_weather_data(current_year, current_month)
    sample_data = myparser.weather_data

    db = DBOperations("weathers.sqlite")
    db.save_data(sample_data)

    # Print out fetch_data output
    # db = DBOperations("weathers.sqlite")
    # data = db.fetch_data()
    # print(data)

if __name__=="__main__":
    main()
    