import urllib.parse
import urllib.request
import json
import time
#import display

# API key to use for requests
API_KEY = "vxQXe7TxHtVtJc4FLAns2bQxp"

# which of the system's data feeds to use
DATA_FEED = "Port Authority Bus"

# base url for all API requests
API_BASE_URL = "http://truetime.portauthority.org/bustime/api/v3/"
# bus predictions URL
GET_PREDICTIONS_URL = API_BASE_URL+"getpredictions?"

# bus statuses to show
buses = [
    {"name": "75 inbound",
     "route": "75",
     "stop": "3285"
    },
    {"name": "75 outbound",
     "route": "75",
     "stop": "19125"
    }
]

# time between API requests, in seconds
TIME_BETWEEN_REQUESTS = 60


# make a getpredictions API request
def get_predictions(rt,stpid):
    request_url = GET_PREDICTIONS_URL

    request_params = {'key': API_KEY,
                      'rt': rt,
                      'stpid': stpid,
                      'rtpidatafeed': DATA_FEED,
                      'format': 'json'}

    full_request_url = request_url + urllib.parse.urlencode(request_params)

#    print(full_request_url)

    with urllib.request.urlopen(full_request_url) as response:
        json_data = response.read()

    # convert json to native
    data = json.loads(json_data)
#    print(data)

    return data


def loop():
    for bus in buses:
        api_response = get_predictions(bus['route'],bus['stop'])
        print (api_response)
        if 'error' in api_response['bustime-response']:
            # one or more errors were received in the response
            errors = api_response['bustime-response']['error']
            for error in errors:
                print(error['msg'])
                
        eta = "###"
        if 'prd' in api_response['bustime-response']:
            prediction = api_response['bustime-response']['prd'][0]
            eta = prediction["prdctdn"]
            if eta.isdigit():
                eta += "m"

        eta_text = "{:12} {:>4}".format(bus["name"],
                                        eta)
        print(eta_text)

def main():
    while True:
        loop()
        print("")
        time.sleep(TIME_BETWEEN_REQUESTS)
                


try:
    main()
except KeyboardInterrupt:
    pass
finally:
    display.end()
