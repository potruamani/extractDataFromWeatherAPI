import datetime
import json
import urllib.request
import webbrowser
import os
import threading
import logging
import sys

from pymongo import MongoClient
from config import config_dict

# set the basic config stdout to INFO
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# establish a connection between mongodb client and server
client = MongoClient()
db = client.test
five_day_forecast = db.five_day_forecast
weather_maps = db.weather_maps


# create threads for calling functions
class myThread(threading.Thread):
    def __init__(self, type):
        threading.Thread.__init__(self)
        self.type = type

    def run(self):
        run_required(self.type)


# convert time to HH:MM:SS
def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


# build an url for the 5-day forecast
def url_builder_days(city, country):
    user_api = '2fc074e79f226106e1bcd27c14ebad5f'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/forecast?q={city},{country}'.format(city=city, country=country)
    full_api_url = api + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url


# build url for the weather maps
def url_builder_maps(layer, z, x, y):
    user_api = '2fc074e79f226106e1bcd27c14ebad5f'
    api_maps = 'https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?'.format(layer=layer, z=z, x=x, y=y)
    full_api_url_maps = api_maps + '&APPID=' + user_api
    return full_api_url_maps


# download the maps into perticular forlder and also insert binary data of maps into mongodb records
def fetch_and_download_map(full_api_url_maps, city, country):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    weather_maps_dir = os.path.join(current_dir, 'weather_maps')
    if not os.path.exists(weather_maps_dir):
        os.mkdir(weather_maps_dir)

    binary_image_data = urllib.request.urlopen(full_api_url_maps).read()
    f = open(weather_maps_dir + '/' + city + '_' + country + '.png', 'wb')
    f.write(binary_image_data)
    f.close()

    map_dict = {'city': city, 'country': country, 'image': binary_image_data}
    weather_maps.insert(map_dict)


def run_required(type):
    if type == 'days':
        for loc in config_dict['locations']:
            url_days = url_builder_days(loc['city'], loc['country'])
            fetch_and_insert_in_mongo(url_days)
    elif type == 'maps':
        for i, loc in enumerate(config_dict['locations']):
            url_maps = url_builder_maps('clouds', loc['z'], loc['x'], loc['y'])
            fetch_and_download_map(url_maps, loc['city'], loc['country'])
            # if i==len(config_dict['locations'])-1:
            webbrowser.open_new_tab(url_maps)


# insert the 5-day forecast data into the mongodb records
def fetch_and_insert_in_mongo(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    update_dict = {'city': raw_api_dict['city']['name'],
                   'country': raw_api_dict['city']['country']}

    for record in raw_api_dict['list']:
        record.update(update_dict)
        five_day_forecast.insert(record)
        check_weather_cond(record)


# print the info to the cli outpurt based on weather conditions
def check_weather_cond(record):
    for weather in record['weather']:
        if weather['main'] != 'Clear':
            logging.info("weather looks like {desc} in {city} at {time} on {day}"
                         .format(desc=weather['description'], city=record['city'],
                                 time=time_converter(record.get('dt')), day=record['dt_txt']))

    temp = round(record['main']['temp'])
    if (temp==num for num in range(-15, -18, -1)):
        logging.info("temperature condition of weather is like freezing at {temp} kelvin in {city}"
                     .format(temp=record['main']['temp'], city=record['city']))

# def fetch_data_from_monodb():
#     for data in db.five_day_forecast.find():
#         print(data)


if __name__ == '__main__':
    try:
        t1 = myThread('days')
        t1.start()
        t2 = myThread('maps')
        t2.start()

        t1.join()
        t2.join()
    except IOError as e:
        print(repr(e))
