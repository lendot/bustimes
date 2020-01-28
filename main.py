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

BUS_ROUTES="75"
BUS_STOPS="3285,19125"

# time between API requests, in seconds
TIME_BETWEEN_REQUESTS = 60

# make a getpredictions API request
def get_predictions():
    request_url = GET_PREDICTIONS_URL

    request_params = {'key': API_KEY,
                      'rt': BUS_ROUTES,
                      'stpid': BUS_STOPS,
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

def main():
    while True:

#        display.clear()
        
        api_response = get_predictions()

        print (api_response)

        if 'error' in api_response['bustime-response']:
            # one or more errors were received in the response
            errors = api_response['bustime-response']['error']
            for error in errors:
                print(error['msg'])


        if 'prd' not in api_response['bustime-response']:
            # no route predictions
            print("###")
            continue
            
        predictions = api_response['bustime-response']['prd']
        
        for prediction in predictions:
            predict_time = prediction["prdctdn"]
            if predict_time.isdigit():
                predict_time += "m"
            prediction_text = "{:3} {:8} {:>4}".format(prediction["rt"],
                                                        prediction["rtdir"],
                                                        predict_time)
            print(prediction_text)

        print("")
        time.sleep(TIME_BETWEEN_REQUESTS)


try:
    main()
except KeyboardInterrupt:
    pass
finally:
    display.end()
