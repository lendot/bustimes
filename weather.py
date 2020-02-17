import urllib.parse
import urllib.request
import json

WEATHER_URL_BASE="https://api.darksky.net/forecast"

class Weather:
    """
    Interface to the Dark Sky weather API.
    """
    def __init__(self,api_key,lat,lng):
        """
        Constructor for Weather.

        Parameters:
          api_key: the Dark Sky API key.
          lat: latitude for the weather location.
          lng: longitude for the weather location.
        """
        
        self.lat = lat
        self.lng = lng
        self.api_key = api_key
        self.url = "{}/{}/{},{}".format(WEATHER_URL_BASE,api_key,lat,lng)

    def get_weather(self):
        """
        Queries the API and returns current and today weather data
        """
        with urllib.request.urlopen(self.url) as response:
            json_data = response.read().decode('utf-8')
        data = json.loads(json_data)

        weather = {}
        weather['current'] = {
            'temp': round(data['currently']['temperature']),
            'summary': data['currently']['summary']
        }
        today = data['daily']['data'][0]
        weather['today'] = {
            'temp': round(today['temperatureHigh']),
            'summary': today['summary']
        }
        
        return weather
    
