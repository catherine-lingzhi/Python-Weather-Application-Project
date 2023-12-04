"""
Description: Final Project Part 2 -Database
Date: 2023-11-09
Usage: Create a DBOperations class to create a database using DBCM class.
Group 7: Lingzhi Luo and Alem Bade Bene
"""
import logging
from datetime import datetime
from dbcm import DBCM

logging.basicConfig(filename='db_operations.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class DBOperations:
    """Class for performing operations on a weather data SQLite database."""
    def __init__(self, db_name):
        """Initializes the DBOperations instance with the specified database name."""
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        """Creates the 'weather_data' table if it doesn't exist in the database."""
        try:
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
        except Exception as e:
            logging.error("Error initializing database: %s", e)

    def purge_data(self):
        """Deletes all data from the 'weather_data' table."""
        try:
            with DBCM(self.db_name) as cursor:
                cursor.execute('DELETE FROM weather_data')
        except Exception as e:
            logging.error("Error purging data: %s", e)

    def save_data(self, sample_data):
        """Saves weather data to the 'weather_data' table."""
        try:
            with DBCM(self.db_name) as cursor:
                for date, values in sample_data.items():
                    location = "Winnipeg"  # Corrected typo in location name
                    min_temp = values.get("Min")
                    max_temp = values.get("Max")
                    avg_temp = values.get("Mean")

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
        except Exception as e:
            logging.error("Error saving data to database: %s", e)

    def fetch_data(self):
        """Retrieves data from the 'weather_data' table for creating plots."""
        plotter_data = {}
        try:
            with DBCM(self.db_name) as cursor:
                cursor.execute('SELECT sample_date, avg_temp FROM weather_data')
                data_from_db = cursor.fetchall()

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
                    logging.error("Error: Unable to parse date %s. %s", date, e)
                    continue

        except Exception as e:
            logging.error("Error fetching data: %s", e)

        return plotter_data

def print_data():
    """Fetch all data from the URL."""
    try:
        with DBCM("weathers.sqlite") as cursor:
            cursor.execute('SELECT MAX(date(sample_date)) FROM weather_data;')
            latest_date = cursor.fetchone()
            print("Latest date from the database:", latest_date)

    except Exception as e:
        logging.error("Error printing data: %s", e)

if __name__ == "__main__":
    print_data()
