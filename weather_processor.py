"""
Description: Final Project Part 2 -Database
Date: 2023-11-26
Usage: Allow the user to download the weather data and enter the 
year month to generate box plot and line plot.
Group 7: Lingzhi Luo and Alem Bade Bene
"""
from db_operations import DBOperations
from plot_operations import PlotOperations
from scrape_weather import WeatherScraper
from datetime import datetime
from dbcm import DBCM
from datetime import timedelta

class WeatherProcessor:
    def __init__(self, db_name="weathers.sqlite"):
        self.db_name = db_name
        self.db_operations = DBOperations(db_name)
        self.plot_operations = PlotOperations(self.db_operations.fetch_data())
        self.weather_scraper = WeatherScraper()

    def show_menu(self):
        """Displays the main menu."""
        print("1. Download Full Set of Weather Data")
        print("2. Update Weather Data")
        print("3. Generate Box Plot")
        print("4. Generate Line Plot")
        print("5. Exit")

    def process_choice(self, choice):
        """Processes user's choice from the menu."""
        try:
            choice = int(choice)
            if choice == 1:
                self.weather_scraper.fetch_all_data()
                self.db_operations.save_data(self.weather_scraper.weather_data)
                print("Weather data downloaded and saved.")
            elif choice == 2:
                # Fetch the latest date directly from the database
                with DBCM(self.db_name) as cursor:
                    cursor.execute('SELECT MAX(date(sample_date)) FROM weather_data')
                    result = cursor.fetchone()                    

                latest_date_str = result[0]             
                latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d").date()
                current_date = datetime.now().date()               

                if latest_date <= current_date:
                    self.weather_scraper.fetch_update_data(latest_date.year, latest_date.month)
                    new_data = self.weather_scraper.weather_data
                    self.db_operations.save_data(new_data)
                    print(f"Weather data updated from {latest_date} to latest date on website")             
             
            elif choice == 3:
                start_year = int(input("Enter the starting year: "))
                end_year = int(input("Enter the ending year: "))
                self.plot_operations.create_boxplot(start_year, end_year)
            elif choice == 4:
                year = int(input("Enter the year: "))
                month = int(input("Enter the month: "))
                self.plot_operations.create_lineplot(year, month)
            elif choice == 5:
                print("Exiting the program.")
                exit()
            else:
                print("Invalid choice. Please choose a number from 1 to 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def run(self):
        """Runs the WeatherProcessor."""
        while True:
            self.show_menu()
            try:
                choice = int(input("Enter your choice: "))
                self.process_choice(choice)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    weather_processor = WeatherProcessor()
    weather_processor.run()
