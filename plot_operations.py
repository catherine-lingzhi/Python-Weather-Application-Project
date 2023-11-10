import matplotlib.pyplot as plt

class PlotOperations:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def create_boxplot(self, start_year, end_year):
        # Extract mean temperatures for each month within the date range
        monthly_means = {month: [] for month in range(1, 13)}

        for year in range(start_year, end_year + 1):
            for date, temperatures in self.weather_data.get(year, {}).items():
                month = int(date.split('-')[1])
                monthly_means[month].extend(temperatures["Mean"])

        # Create boxplot
        plt.boxplot(monthly_means.values(), labels=[str(month) for month in range(1, 13)])
        plt.xlabel('Month')
        plt.ylabel('Mean Temperature (°C)')
        plt.title('Boxplot of Mean Temperatures by Month')
        plt.show()

    def create_lineplot(self, year, month):
        # Extract mean temperatures for the specified year and month
        daily_means = self.weather_data.get(year, {}).get(f"{year}-{month:02d}", {}).get("Mean", [])

        # Create lineplot
        plt.plot(range(1, len(daily_means) + 1), daily_means, marker='o')
        plt.xlabel('Day')
        plt.ylabel('Mean Temperature (°C)')
        plt.title(f'Lineplot of Mean Temperatures for {year}-{month:02d}')
        plt.show()

# Example usage
if __name__ == "__main__":
    # Example weather_data (replace this with your actual data)
    weather_data = {
        2020: {"2020-01-01": {"Mean": [5.0, 6.2, 4.8]}, "2020-01-02": {"Mean": [3.9, 5.1, 2.5]}, ...},
        2021: {"2021-01-01": {"Mean": [4.8, 5.9, 3.4]}, "2021-01-02": {"Mean": [2.7, 4.3, 1.8]}, ...},
        # ...
    }

    plotter = PlotOperations(weather_data)

    # Create a boxplot for the date range 2000 to 2020
    plotter.create_boxplot(2000, 2020)

    # Create a lineplot for January 2021
    plotter.create_lineplot(2021, 1)

