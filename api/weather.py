import numpy as np
import openmeteo_requests
import requests_cache
from retry_requests import retry

class WeatherDataFetcher:
    def __init__(self):
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)

    # Takes the given information and returns the corresponding weather data
    def fetch_weather_data(self, latitude, longitude, start_date, end_date):
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "snowfall_sum",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "America/Denver"
        }
        return self.openmeteo.weather_api(url, params=params)

    # Takes the given weather data and parses it, so it can be used
    def process_weather_data(self, response):
        latitude = np.float_(response.Latitude())
        longitude = np.float_(response.Longitude())

        daily = response.Daily()
        daily_snowfall_sum = np.float_(daily.Variables(0).ValuesAsNumpy().sum())

        list = [latitude, longitude, daily_snowfall_sum]

        return list
