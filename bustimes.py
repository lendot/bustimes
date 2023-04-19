import logging
import tkinter as tk
import tkinter.font as tkfont
import yaml
import weatherapi
import bus

CONFIG_FILE = "config.yaml"

LOG_FILE = "bustimes.log"

FONT_FAMILY = "Ubuntu Mono"

class BusTimes(tk.Frame):

    def __init__(self, root, bus_service, weather_service, config):
        super().__init__(root)
        # make window full screen
        w,h = root.winfo_screenwidth(), root.winfo_screenheight()
        # get rid of title bar, etc.
        root.overrideredirect(1)
        root.geometry("{0}x{1}+0+0".format(w,h))
        root.config(bg="black")

        self.root = root
        self.bus_service = bus_service
        self.weather_service = weather_service
        self.config = config
        self.create_ui()

    def create_ui(self):
        self.bus_frame = tk.Frame(self.root,bg="black",padx=50,pady=50)
        self.bus_frame.grid_columnconfigure(0,weight=1)
        self.bus_frame.grid_columnconfigure(1,weight=1)
        self.bus_frame.grid_columnconfigure(2,weight=1)
        self.bus_frame.pack(expand=True, fill='both')
        
        self.bus_view = self.BusView(self.bus_frame,
                                     self.bus_service,
                                     self.config)
        
        self.weather_frame = tk.Frame(self.root,padx=50,bg="black")
        self.weather_frame.grid_columnconfigure(0,weight=1)
        self.weather_frame.grid_columnconfigure(1,weight=1)
        self.weather_frame.pack(expand=True, fill='both')
        
        self.weather_view = self.WeatherView(self.weather_frame,
                                             self.weather_service,
                                             self.config)


    class BusView:

        def __init__(self,frame,bus_service,config):
            self.frame = frame
            self.bus_routes = config['bus']['route']
            self.bus_service = bus_service
            self.config = config
            self.bus_font = tkfont.Font(family=FONT_FAMILY,size=100)
            self.colors={}
            self.colors["name"]="#9b4f96"
            self.colors["direction"]="#0038a8"
            self.colors["due"]="#d60270"
            self.create_cells()
            self.update()


        def create_label(self,frame,text,fg):
            label = tk.Label(frame,
                             text=text,
                             fg=fg,
                             bg="black",
                             font=self.bus_font)
            return label
    
        
        def create_cells(self):
            for r, bus in enumerate(self.bus_routes):
                name_label = self.create_label(self.frame,
                                               bus['route'],
                                               self.colors["name"])
                name_label.grid(column=0,row=r,sticky=tk.W)
                bus['name_label'] = name_label
                
                direction_label = self.create_label(self.frame,
                                                    bus['direction'],
                                                    self.colors["direction"])
                direction_label.grid(column=1,row=r,sticky=tk.W)
                bus['direction_label'] = direction_label
                
                due_label = self.create_label(self.frame,
                                              "---",
                                              self.colors["due"])
                due_label.grid(column=2,row=r,sticky=tk.E)
                bus['due_label'] = due_label
            

        def update(self):
            for bus in self.bus_routes:
                try:
                    api_response = self.bus_service.get_predictions(bus['route'],bus['stop'])
                except Exception as e:
                    # catch-all for anything that goes wrong with fetching the data
                    logging.exception("Bus update error")
                    bus['due_label']['text'] = "err"
                    continue
                    
                eta = "---"
                if 'prd' in api_response['bustime-response']:
                    # we have a prediction
                    prediction = api_response['bustime-response']['prd'][0]
                    eta = prediction["prdctdn"]
                    if eta.isdigit():
                        eta += "m"
                bus['due_label']['text'] = eta
            self.frame.after(self.config['bus']['time_between_requests']*1000,
                             self.update)
            
                
    class WeatherView:
                        
        def __init__(self,frame,weather_service,config):
            self.frame = frame
            self.weather_service = weather_service
            self.config = config

            # set up fonts
            self.label_font = tkfont.Font(family=FONT_FAMILY,size=30)
            self.summary_font = tkfont.Font(family=FONT_FAMILY,size=40)
            self.temperature_font = tkfont.Font(family=FONT_FAMILY,size=75)

            # set up colors
            self.colors = {}
            self.colors["summary"]="#9b4f96"
            self.colors["label"]="#0038a8"
            self.colors["temperature"]="#d60270"
            
            self.create_frames()
            self.create_cells()
            self.update()
            
        def create_frames(self):
            self.frame_current = tk.Frame(self.frame,bg="black",padx=50)
            self.frame_current.grid(row=0,column=0,sticky=tk.N)
            self.frame_forecast = tk.Frame(self.frame,bg="black",padx=50)
            self.frame_forecast.grid(row=0,column=1,sticky=tk.N)
            
        def create_label(self,frame,text,fg,font):
            label = tk.Label(frame,
                             text=text,
                             fg=fg,
                             bg="black",
                             font=font)
            return label
                
        def create_cells(self):
            self.label_current = self.create_label(self.frame_current,
                                                   "Current",
                                                   self.colors["label"],
                                                   self.label_font)
            self.label_current.grid(column=0,row=0)
            
            self.label_current_temp = self.create_label(self.frame_current,
                                                        "---",
                                                        self.colors["temperature"],
                                                        self.temperature_font)
            self.label_current_temp.config(pady=20)
            self.label_current_temp.grid(column=0,row=1)
            
            self.label_current_summary = self.create_label(self.frame_current,
                                                           "---",
                                                           self.colors["summary"],
                                                           self.summary_font)
            self.label_current_summary.config(wraplength=700)
            self.label_current_summary.grid(column=0,row=2)
            
            
            self.label_today = self.create_label(self.frame_forecast,
                                                 "Today",
                                                 self.colors["label"],
                                                 self.label_font)
            self.label_today.grid(column=0,row=0)
            
            self.label_today_temp = self.create_label(self.frame_forecast,
                                                      "---",
                                                      self.colors["temperature"],
                                                      self.temperature_font)
            self.label_today_temp.config(pady=20)
            self.label_today_temp.grid(column=0,row=1)
            
            self.label_today_summary = self.create_label(self.frame_forecast,
                                                         "---",
                                                         self.colors["summary"],
                                                         self.summary_font)
            self.label_today_summary.config(wraplength=700)
            self.label_today_summary.grid(column=0,row=2)
                    
        def update(self):
            success = True
            try:
                weather = self.weather_service.get_weather()
            except Exception as e:
                # catch-all for anything that goes wrong with fetching the data
                logging.exception("Weather update error")
                success = False

            if success:
                self.label_current_temp['text'] = weather['current']['temp']
                self.label_current_summary['text'] = "{} {}% hum.".format(
                        weather['current']['summary'],weather['current']['humidity'])
                self.label_today_temp['text'] = weather['today']['temp']
                self.label_today_summary['text'] = weather['today']['summary']
            else:
                self.label_current_temp['text'] = "err"
                self.label_current_summary['text'] = "---"
                self.label_today_temp['text'] = "err"
                self.label_today_summary['text'] = "---"
                
            self.frame.after(self.config['weather']['time_between_requests']*1000,
                             self.update)


def main():

    logging.basicConfig(filename=LOG_FILE,
                        level=logging.INFO,
                        format='%(asctime)s %(message)s')
    logging.info("Bustimes starting")
    
    with open('config.yaml') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
    weather_api_key = config['weather']['api_key']
    lat = config['weather']['latitude']
    lng = config['weather']['longitude']
    logging.info('Weather API: %s',weather_api_key)
    logging.info('Weather latitude: %s',lat)
    logging.info('Weather longitude: %s',lng)
    weather_service = weatherapi.WeatherApi(weather_api_key,
                                      lat,
                                      lng)
    bus_api_key = config['bus']['api_key']
    bus_api_base_url = config['bus']['api_base_url']
    bus_data_feed = config['bus']['data_feed']
    logging.info('Bus API: %s',bus_api_key)
    logging.info("Bus API base URL: %s",bus_api_base_url)
    logging.info("Bus API data feed: %s",bus_data_feed)
    bus_service = bus.Bus(bus_api_key,
                          bus_api_base_url,
                          bus_data_feed)

    window = tk.Tk()
    
    app = BusTimes(window,bus_service,weather_service,config)

    window.mainloop()

    logging.info("Bustimes exiting")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("main exception")
    finally:
        logging.info("Exiting")
