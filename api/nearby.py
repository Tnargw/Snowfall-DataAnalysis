import requests

class NearbyCities:
    def __init__(self, radius=100, max_results=10):
        self.radius = radius
        self.max_results = max_results

    # Takes a given starting point and returns a list of nearby cities
    def get_nearby_cities_geonames(self, latitude, longitude):
        try:
            username = 'tnargw'
            url = f"http://api.geonames.org/findNearbyPlaceNameJSON?formatted=true&lat={latitude}&lng={longitude}&radius={self.radius}&maxRows={self.max_results}&username={username}&cities=cities1000"
            response = requests.get(url)
            data = response.json()
            if 'geonames' in data:
                nearby_cities = {}
                for place in data['geonames']:
                    name = place['name']
                    latitude = place['lat']
                    longitude = place['lng']
                    nearby_cities[name] = latitude, longitude
                    print('Nearby location found:', name, latitude, longitude)
                return nearby_cities   # Return key/value pairs (city name and distance)
            else:
                print("No 'geonames' key found in response")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
