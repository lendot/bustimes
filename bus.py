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

    def __init__(self,api_key):
        self.api_key = api_key

    # make a getpredictions API request
    def get_predictions(self,rt,stpid):
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

