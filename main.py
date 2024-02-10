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


    input_lat, input_lon = map_generator.get_location(address)

    nearbyCities = NearbyCities()
    nearby_data = nearbyCities.get_nearby_cities_geonames(input_lat, input_lon)

    data = []
    for key, coords in nearby_data.items():
        address = f"{coords[0]}, {coords[1]}"

        weather_fetcher = WeatherDataFetcher()
        responses = weather_fetcher.fetch_weather_data(coords[0], coords[1], start_date, end_date)

        for response in responses:
            response_dataframe = weather_fetcher.process_weather_data(response)

            if [response_dataframe[0], response_dataframe[1], response_dataframe[2]] in data:
                print(response_dataframe[0], response_dataframe[1], response_dataframe[2], 'Already Processed')
            else:
                data.append([response_dataframe[0], response_dataframe[1], response_dataframe[2]])

            m = map_generator.get_map(address)
    map_generator.add_heat_map(m, data)
    map_generator.open_map(m)
