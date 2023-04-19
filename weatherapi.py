import urllib.parse
import urllib.request
import json

# WEATHER_URL_BASE="https://api.darksky.net/forecast"
WEATHER_URL_BASE="http://api.weatherapi.com/v1/forecast.json"

class WeatherApi:
    """
    Interface to WeatherAPI.
    """
    def __init__(self,api_key,lat,lng):
        """
        Constructor for WeatherApi.

        Parameters:
          api_key: the WeatherAPI key.
          lat: latitude for the weather location.
          lng: longitude for the weather location.
        """
        
        self.lat = lat
        self.lng = lng
        self.api_key = api_key
        self.url = f"{WEATHER_URL_BASE}?key={api_key}&q={lat},{lng}"

    def get_weather(self):
        """
        Queries the API and returns current and today weather data
        """
        with urllib.request.urlopen(self.url) as response:
            json_data = response.read().decode('utf-8')

        data = json.loads(json_data)

        weather = {}
        weather['current'] = {
            'temp': round(data['current']['temp_f']),
            'humidity': round(data['current']['humidity']),
            'summary': data['current']['condition']['text']
        }
        today = data['forecast']['forecastday'][0]['day']
        weather['today'] = {
            'temp': round(today['maxtemp_f']),
            'summary': today['condition']['text']
        }
        
        return weather
    
