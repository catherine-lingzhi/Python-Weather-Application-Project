from html.parser import HTMLParser
import urllib.request
from datetime import datetime
import re

class WeatherScraper(HTMLParser):
    """A class for scraping weather data from a website."""

    def __init__(self):
        """Initialize the WeatherScraper instance."""
        super().__init__() 
        self.in_h1 = False       
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
        if tag == 'h1':
            self.in_h1 = True
        elif tag == 'tr':
            self.in_tr = True
            self.td_count = 0            
        elif self.in_tr and tag == 'td':
            self.in_td = True
        elif self.in_tr and tag == 'th':
            self.in_th = True

    def handle_endtag(self, tag):
        """Handle the end tag of an HTML element."""
        if tag == 'h1':
            self.in_h1 = False
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
        if self.in_h1:
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

    def scrape_weather_data_from_url(self, url):
        """Scrape weather data from a specific URL."""
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        self.feed(html)      

    def fetch_all_data(self, current_year=datetime.now().year, current_month=datetime.now().month):
        """Fetch all data from the website"""
        while True:
            url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={current_year}&Day=1&Year={current_year}&Month={current_month}#"
            self.scrape_weather_data_from_url(url)

            # Check the condition to stop the loop
            if self.year == current_year and self.month != current_month:
                break

            # Move to the previous month
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1   

    def fetch_update_data(self, start_year, start_month):
        """Fetch update data from the website"""
        current_year=datetime.now().year
        current_month=datetime.now().month

        while True:
            url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={current_year}&Day=1&Year={current_year}&Month={current_month}#"
            self.scrape_weather_data_from_url(url)

            # Check the condition to stop the loop
            if current_year == start_year and current_month == start_month:
                break

            # Move to the previous month
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1           
def main():
    """Main function to demonstrate the usage."""
    my_parser = WeatherScraper()   
    my_parser.fetch_update_data(2023, 10)
    print(my_parser.weather_data)
if __name__ == "__main__":
    main()

