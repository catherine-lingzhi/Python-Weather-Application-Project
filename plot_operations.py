"""
Description: Final Project- Part 3 - Plotting
Date: 2023-11-29
Usage: This script defines a PlotOperations class to create box plots and line plots
       based on weather data retrieved from an SQLite database using DBOperations class.
Group 7: Lingzhi Luo and Alem Bade Bene
"""
import logging
import matplotlib.pyplot as plt
from db_operations import DBOperations

logging.basicConfig(filename='plot_operations.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class PlotOperations:
    """Class for creating box plots and line plots based on weather data."""
    def __init__(self, weather_data):
        """Initializes the PlotOperations instance with the provided weather data."""
        self.weather_data = weather_data

    def create_boxplot(self, start_year, end_year):
        """Creates a box plot of monthly temperature distributions within a specified date range."""
        if self.weather_data is None:
            print("No weather data available.")
            return

        monthly_means = {month: [] for month in range(1, 13)}

        for year in range(start_year, end_year + 1):
            for month, days in self.weather_data.get(year, {}).items():
                for avg_temp in days.values():
                    if avg_temp is not None:
                        monthly_means[int(month)].append(avg_temp)

        for month, values in monthly_means.items():
            if not values:
                print(f"No data available for {start_year}-{month:02d}")

        plt.boxplot(monthly_means.values(), labels=[str(month) for month in range(1, 13)])
        plt.xlabel('Month')
        plt.ylabel('Mean Temperature (°C)')
        plt.title(f'Monthly Temperature Distribution for:{start_year} to {end_year}')
        plt.show()

    def create_lineplot(self, year, month):
        """Creates a line plot of daily average temperatures for a specified year and month."""
        if self.weather_data is None:
            print("No weather data available.")
            return

        daily_means = [
            avg_temp
            for avg_temp in self.weather_data.get(year, {}).get(month, {}).values()
            if avg_temp is not None  # Check for missing values
        ]

        if not daily_means:
            print(f"No data available for {year}-{month:02d}")
            return

        days = list(self.weather_data.get(year, {}).get(month, {}).keys())
        dates = [f'{year}-{month:02d}-{day:02d}' for day in days]
        plt.plot(dates, daily_means)
        plt.xlabel(f'Daily of {month}')
        plt.ylabel('Average Daily Temp (°C)')
        plt.title('Daily Avg Temperatures')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        plt.show()

# Example usage
def main():
    """Create line plot and box plot."""
    db = DBOperations("weathers.sqlite")
    plotter_data = db.fetch_data()
    plotter = PlotOperations(plotter_data)

    # Create a boxplot for the date range 2000 to 2020
    plotter.create_boxplot(2000, 2017)

    # Create a lineplot for January 2021
    plotter.create_lineplot(2020, 3)

if __name__ == "__main__":
    main()
