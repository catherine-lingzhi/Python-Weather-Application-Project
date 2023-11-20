"""
Description: Final Project- Part 1 Scraping
Date: 2023-11-06
Usage: Create an WeatherScraper class to fet weather data from a website.
Group 7: Lingzhi Luo and Alem Bade Bene
"""
from html.parser import HTMLParser
import urllib.request
from datetime import datetime
import re

class WeatherScraper(HTMLParser):
    """A class for scraping weather data from a website."""
    def __init__(self):
        """Initialize the WeatherScraper instance."""
        super().__init__() 
        self.in_caption = False       
        self.in_tr = False
        self.in_td = False
        self.in_th = False     
        self.td_count = 0
        self.day = None
        self.year = None
        self.month = None
        self.daily_temps = {"Max": None, "Min": None, "Mean": None}
        self.weather_data = {}

    def handle_starttag(self, tag, attrs):
        """Handle the start tag of an HTML element."""
        if tag == 'caption':
            self.in_caption = True
        elif tag == 'tr':
            self.in_tr = True
            self.td_count = 0            
        elif self.in_tr and tag == 'td':
            self.in_td = True
        elif self.in_tr and tag == 'th':
            self.in_th = True

    def handle_endtag(self, tag):
        """Handle the end tag of an HTML element."""
        if tag == 'caption':
            self.in_caption = False
        elif tag == 'tr':
            self.in_tr = False
            if self.day:
                self.weather_data[f"{self.year}-{self.month}-{self.day}"] = {
                    "Max": self.daily_temps["Max"],
                    "Min": self.daily_temps["Min"],
                    "Mean": self.daily_temps["Mean"]
                }
            self.day = None
        elif tag == 'td':
            self.in_td = False
            self.td_count += 1
        elif tag == 'th':
            self.in_th = False

    def handle_data(self, data):
        """Handle the data within an HTML element."""  
        if self.in_caption:
            self.extract_month_and_year(data)
        if self.in_th:
            if data.isdigit():
                self.day = int(data)      
        if self.in_td and self.td_count < 3:
            if self.td_count == 0:
                self.daily_temps["Max"] = self.try_parse_float(data)
            elif self.td_count == 1:
                self.daily_temps["Min"] = self.try_parse_float(data)
            elif self.td_count == 2:
                self.daily_temps["Mean"] = self.try_parse_float(data)

    def try_parse_float(self, value):
        """Try to parse a string as a float and return None if it is not a valid float."""
        try:
            return float(value)
        except ValueError:
            return None

    def extract_month_and_year(self, input_string):
        """Convert literal month to int."""  
        month_mapping = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12
        }        
        match = re.search(r'(\w+) (\d+)', input_string)

        if match:
            month_name = match.group(1)
            self.month = int(month_mapping.get(month_name))
            self.year = int(match.group(2))

    def scrape_weather_data(self, year, month):
        """Scrape weather data for a specific year and month."""      
        while self.year != year or self.month != month:
            url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={year}&Day=1&Year={year}&Month={month}#"
            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')
            self.feed(html)
            # print(self.weather_data)

            if self.year != year or self.month != month:
                break

            month -= 1
            if month == 0:
                month = 12
                year -= 1                         
def print_weather():
    """Print out the weather data"""
    current_year = datetime.now().year
    current_month = datetime.now().month    
    myparser = WeatherScraper()
    myparser.scrape_weather_data(current_year, current_month)   
    # weather = myparser.weather_data
    # print(weather)
if __name__ == "__main__":
    print_weather()
