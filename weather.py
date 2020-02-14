import urllib.parse
import urllib.request
import json

WEATHER_URL_BASE="https://api.darksky.net/forecast"

class Weather:

    def __init__(self,api_key,lat,lng):
        self.lat = lat
        self.lng = lng
        self.api_key = api_key
        self.url = "{}/{}/{},{}".format(WEATHER_URL_BASE,api_key,lat,lng)

    def get_weather(self):
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
    
