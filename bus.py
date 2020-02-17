import urllib.parse
import urllib.request
import json

# which of the system's data feeds to use
DATA_FEED = "Port Authority Bus"
# base url for all API requests
API_BASE_URL = "http://truetime.portauthority.org/bustime/api/v3/"
# bus predictions URL
GET_PREDICTIONS_URL = API_BASE_URL+"getpredictions?"

class Bus:
    """
    Interface to the BusTime bus tracking API.
    """
    
    def __init__(self,api_key):
        """
        Constructor for Bus.

        Parameters:
          api_key: The BusTime API key.
        """
        self.api_key = api_key

    def get_predictions(self,rt,stpid):
        """
        Get a bus arrival prediction.
        
        Parameters:
          rt: the bus route
          stpid: the stop id
        """
        request_url = GET_PREDICTIONS_URL

        request_params = {'key': self.api_key,
                          'rt': rt,
                          'stpid': stpid,
                          'rtpidatafeed': DATA_FEED,
                          'format': 'json'}

        full_request_url = request_url + urllib.parse.urlencode(request_params)

        with urllib.request.urlopen(full_request_url) as response:
            json_data = response.read().decode('utf-8')

            # convert json to native
            data = json.loads(json_data)
            return data

