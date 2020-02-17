import urllib.parse
import urllib.request
import json

# which of the system's data feeds to use
#DATA_FEED = "Port Authority Bus"
# base url for all API requests
#API_BASE_URL = "http://truetime.portauthority.org/bustime/api/v3/"
# bus predictions URL
#GET_PREDICTIONS_URL = API_BASE_URL+"getpredictions?"

class Bus:
    """
    Interface to the BusTime bus tracking API.
    """
    
    def __init__(self,api_key,api_base_url,data_feed):
        """
        Constructor for Bus.

        Parameters:
          api_key: The BusTime API key.
          api_base_url: base URL for API requests.
          data_feed: which of the BusTime system's data feeds to use.
        """
        self.api_key = api_key
        self.api_base_url = api_base_url
        self.data_feed = data_feed
        self.get_predictions_url = self.api_base_url + "getpredictions?"

    def get_predictions(self,rt,stpid):
        """
        Get a bus arrival prediction.
        
        Parameters:
          rt: the bus route
          stpid: the stop id
        """
        request_url = self.get_predictions_url

        request_params = {'key': self.api_key,
                          'rt': rt,
                          'stpid': stpid,
                          'rtpidatafeed': self.data_feed,
                          'format': 'json'}

        full_request_url = request_url + urllib.parse.urlencode(request_params)
        print(full_request_url)

        with urllib.request.urlopen(full_request_url) as response:
            json_data = response.read().decode('utf-8')

            # convert json to native
            data = json.loads(json_data)
            return data

