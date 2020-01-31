import urllib.parse
import urllib.request
import json
import time
import display
import sys

# API key to use for requests
if len(sys.argv) > 1:
    API_KEY = sys.argv[1]
else:
    print("Usage: python3 main.py API_KEY")
    exit(1)

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


disp = display.Display()

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
        json_data = response.read().decode('utf-8')

    # convert json to native
#    print(json_data)
    data = json.loads(json_data)
#    print(data)

    return data


def loop():
    disp.clear()
    error_msgs=[]
    for bus in buses:
        try: 
            api_response = get_predictions(bus['route'],bus['stop'])
        except Exception as e:
            # catch-all for anything that goes wrong with fetching the data
            disp.text("Error")
            print()
            print()
            print(e)
            return


        # print (api_response)
        if 'error' in api_response['bustime-response']:
            # one or more errors were received in the response
            errors = api_response['bustime-response']['error']
            error_msgs.extend(errors)
                
        eta = "---"
        if 'prd' in api_response['bustime-response']:
            prediction = api_response['bustime-response']['prd'][0]
            eta = prediction["prdctdn"]
            if eta.isdigit():
                eta += "m"

        eta_text = "{:12} {:>4}".format(bus["name"],eta)
#        print(eta_text)
        disp.text(eta_text)

    if len(error_msgs) > 0:
        print()
        print()
        for error in error_msgs:
            print(error)
        
def main():
    while True:
        loop()
        time.sleep(TIME_BETWEEN_REQUESTS)
                


try:
    main()
except KeyboardInterrupt:
    pass
finally:
    disp.end()
