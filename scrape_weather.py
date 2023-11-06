"""
Description: Final Project- Part 1 Scraping
Date: 2023-11-06
Usage: Create an WeatherScraper class to fet weather data from a website.
Group 7: Lingzhi Luo and Alem Bade Bene
"""
from html.parser import HTMLParser
import urllib.request

class WeatherScraper(HTMLParser):
    """A class for scraping weather data from a website."""
    def __init__(self):
        """Initialize the WeatherScraper instance."""
        super().__init__()
        self.in_tr = False
        self.in_td = False
        self.in_th = False
        self.in_a = False
        self.td_count = 0
        self.day = None
        self.year = None
        self.month = None
        self.daily_temps = {"Max": None, "Min": None, "Mean": None}
        self.weather_data = {}

    def handle_starttag(self, tag, attrs):
        """Handle the start tag of an HTML element."""
        if tag == 'tr':
            self.in_tr = True
            self.td_count = 0
            self.daily_temps = {"Day": None, "Max": None, "Min": None, "Mean": None}
        elif self.in_tr and tag == 'td':
            self.in_td = True
        elif self.in_tr and tag == 'th':
            self.in_th = True
        elif self.in_th and tag == 'a':
            self.in_a = True

    def handle_endtag(self, tag):
        """Handle the end tag of an HTML element."""
        if tag == 'tr':
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
        elif tag == 'a':
            self.in_a = False

    def handle_data(self, data):
        """Handle the data within an HTML element."""
        if self.in_a:        
            try:
                self.day = int(data)
            except ValueError:
                self.day = None
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

    def scrape_weather_data(self, year, month):
        """Scrape weather data for a specific year and month."""
        self.year = year
        self.month = month
        url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={year}&Day=1&Year={year}&Month={month}#"
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        self.feed(html)

def print_weather():
    """Print out the weather data"""
    myparser = WeatherScraper()
    myparser.scrape_weather_data(2018, 5)
    weather = myparser.weather_data
    print(weather)

if __name__ == "__main__":
    print_weather()
