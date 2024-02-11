from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap
import webbrowser


class MapGenerator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="map_generator")

    # Returns the latitude and longitude of any address
    def get_location(self, address):
        location = self.geolocator.geocode(address)
        return location.latitude, location.longitude

    # Returns a folium map
    def get_map(self, address):
        location = self.geolocator.geocode(address)
        if location:
            m = folium.Map(location=[location.latitude, location.longitude], zoom_start=9)
            return m
        else:
            print("Couldn't find the location.")
            return None

    # Adds a heatmap to a given map
    def add_heat_map(self, m, data):

        heat_map = HeatMap(data,
                           min_opacity=0.2,
                           max_opacity=0.9,
                           radius=50, blur=50,
                           max_zoom_start=1)
        heat_map.add_to(m)
        m.save("map.html")

    # Saves the map so it can be viewed
    def save_map(self, address):
        m = self.get_map(address)
        if m:
            m.save("map.html")

    # Opens a given map in a web browser
    def open_map(self, m):
        if m:
            webbrowser.open("map.html")
