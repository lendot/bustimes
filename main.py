import time
import display
import sys
import bus

# API key to use for requests
if len(sys.argv) > 1:
    API_KEY = sys.argv[1]
else:
    print("Usage: python3 main.py API_KEY")
    exit(1)

bus_service = bus.Bus(API_KEY)
    
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


def loop():
    disp.clear()
    error_msgs=[]
    for bus in buses:
        try: 
            api_response = bus_service.get_predictions(bus['route'],bus['stop'])
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
