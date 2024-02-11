from api.map import MapGenerator
from api.weather import WeatherDataFetcher
from api.nearby import NearbyCities

if __name__ == "__main__":
    print("This program will generate a map with a heatmap showing the average snowfall for a given area, along with "
          "nearby areas over a given date range.")
    map_generator = MapGenerator()
    address = input("What Location would you like to see? ")
    start_date = input("Please input start date (YYYY-MM-DD): ")
    end_date = input("Please input end date (YYYY-MM-DD): ")
    print("")

    # Gets the latitude and longitude of the user inputted address
    input_lat, input_lon = map_generator.get_location(address)

    # Uses user inputted address to return nearby cities
    nearbyCities = NearbyCities()
    nearby_data = nearbyCities.get_nearby_cities_geonames(input_lat, input_lon)

    # Parses through the nearby cities
    data = []
    for key, coords in nearby_data.items():
        address = f"{coords[0]}, {coords[1]}"

        # Passes the list of nearby cities to the Historical Weather API
        weather_fetcher = WeatherDataFetcher()
        responses = weather_fetcher.fetch_weather_data(coords[0], coords[1], start_date, end_date)

        # Makes the returned data usable
        for response in responses:
            response_dataframe = weather_fetcher.process_weather_data(response)

            # Makes sure the data hasn't already been added, as sometimes the weather data returned will be for the
            # same spot if locations are too close
            if [response_dataframe[0], response_dataframe[1], response_dataframe[2]] in data:
                print(response_dataframe[0], response_dataframe[1], response_dataframe[2], 'Already Processed')
            else:
                data.append([response_dataframe[0], response_dataframe[1], response_dataframe[2]])

            m = map_generator.get_map(address)
    map_generator.add_heat_map(m, data)
    map_generator.open_map(m)
