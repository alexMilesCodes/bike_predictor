import scrapers
import labelling
import requests as rs
import numpy as np
import matplotlib.pyplot as plt
from timezonefinder import TimezoneFinder
import pandas as pd
import geopy as geo
from datetime import datetime
import pytz


tf = TimezoneFinder()

old = pd.read_csv('weather.csv')
profiles = pd.read_csv('profiles.csv')

# initialise lists to fill what will go in the weather table
races_labelled = []
temp = []
feels_like = []
pressure = []
humidity = []
dew_point = []
clouds = []
wind_speed = []
w_notes = []

races = profiles['Race'].to_list()
for i in

            print(df['Race'][race])
            # weather
            data2 = scrapers.get_race_data_dict([df['Race'][race]], show=False)
            geo_loc = geo.geocoders.Nominatim(user_agent="label_main")
            try:
                data2['dep_lat'] = [geo_loc.geocode(data2['Departure Location'].replace('-', ' ')).latitude]
                data2['dep_long'] = [geo_loc.geocode(data2['Departure Location'].replace('-', ' ')).longitude]
            except:
                data2['dep_lat'] = [input('input dep_lat: ')]
                data2['dep_long'] = [input('input dep_long: ')]
            pee = data2['dep_lat']
            poo = data2['dep_long']
            print(f'dep: {pee}, {poo}')
            if input('type 0 to edit: ') == '0':
                data2['dep_lat'] = [input('input dep_lat: ')]
                data2['dep_long'] = [input('input dep_long: ')]
            try:
                data2['arr_lat'] = [geo_loc.geocode(data2['Arrival Location'].replace('-', ' ')).latitude]
                data2['arr_long'] = [geo_loc.geocode(data2['Arrival Location'].replace('-', ' ')).longitude]
            except:
                data2['arr_lat'] = [input('input arr_lat: ')]
                data2['arr_long'] = [input('input arr_long: ')]
            pee = data2['arr_lat']
            poo = data2['arr_long']
            print(f'arr: {pee}, {poo}')
            if input('type 0 to edit: ') == '0':
                data2['arr_lat'] = [input('input arr_lat: ')]
                data2['arr_long'] = [input('input arr_long: ')]
            data2['timezone'] = [tf.timezone_at(lng=data2['dep_long'], lat=data2['dep_lat'])]
            print('local start time:')
            print(scrapers.value_extract(rs.get(df['Race'][race]).text,
                                         'Start time:</div> <div>',
                                         '<'))
            dt_str = str(data2['Date'][0]) + ' ' + input('type local start time'
                                                         '(format - hh:mm, '
                                                         'median - 12:25): ')
            local_dt = datetime.strptime(dt_str, "%d %B %Y %H:%M")
            tz = pytz.timezone(data2['timezone'][0])
            dt = tz.localize(local_dt)
            x = dt.astimezone(pytz.utc)
            data2['start_unix'] = [(((x-pytz.utc.localize(datetime(1970, 1, 1))).view(int))/1e+9)-3600]
            print(data2['start_unix'][0])
            key = '5ce84b1dcac77029347827d990843b54'
            data2['finish_time'] = [scrapers.value_extract(rs.get(df['Race'][race])
                                                           .text[rs.get(df['Race'][race]).text.find('time ar')+7:],
                                                           'time ar" >', '<')]
            data2['finish_time'] = pd.to_datetime(data2['finish_time'], format='%H:%M:%S').view(int)/1e+9
            data2['finish_unix'] = data2['start_unix'] + data2['finish_time']
            print('start time (unix): ', data2['start_unix'])
            print('race length (seconds): ', data2['finish_time'])
            print('finish time (unix): ', data2['finish_unix'])
            query = input('enter 0 to manually overwrite unix finish, 1 to overwrite both: ')
            if query == '0':
                data2['finish_unix'] = input('enter unix finish: ')
            elif query == '1':
                data2['start_unix'] = input('enter unix start: ')
                data2['finish_time'] = input('enter race length in seconds: ')
                data2['finish_unix'] = data2['start_unix'] + data2['finish_time']
            print('retrieving weather data...')
            lat = data2['dep_lat']
            lon = data2['dep_long']
            time = str(int(data2['start_unix']) + int(0.2 * data2['finish_time']))
            data2['weather_dep'] = [rs.get(f'https://api.openweathermap.org/data/3.0/onecall/timemachine?'
                                           f'lat={lat}&lon={lon}&dt={time}&appid={key}&units=metric').text]
            lat = data2['arr_lat']
            lon = data2['arr_long']
            time = str(int(data2['finish_unix']) - int(0.15 * data2['finish_time']))
            data2['weather_arr'] = [rs.get(f'https://api.openweathermap.org/data/3.0/onecall/timemachine?'
                                           f'lat={lat}&lon={lon}&dt={time}&appid={key}&units=metric').text]
            races_labelled.append()
            temp.append((scrapers.value_extract(data2['weather_dep'], '"temp":', ',') +
                         scrapers.value_extract(data2['weather_arr'], '"temp":', ',') * 2) / 3)
            feels_like.append((scrapers.value_extract(data2['weather_dep'], '"feels_like":', ',') +
                               scrapers.value_extract(data2['weather_arr'], '"feels_like":', ',') * 2) / 3)
            pressure.append((scrapers.value_extract(data2['weather_dep'], '"pressure":', ',') +
                             scrapers.value_extract(data2['weather_arr'], '"pressure":', ',') * 2) / 3)
            humidity.append((scrapers.value_extract(data2['weather_dep'], '"humidity":', ',') +
                             scrapers.value_extract(data2['weather_arr'], '"humidity":', ',') * 2) / 3)
            dew_point.append((scrapers.value_extract(data2['weather_dep'], '"dew_point":', ',') +
                              scrapers.value_extract(data2['weather_arr'], '"dew_point":', ',') * 2) / 3)
            clouds.append((scrapers.value_extract(data2['weather_dep'], '"clouds":', ',') +
                           scrapers.value_extract(data2['weather_arr'], '"clouds":', ',') * 2) / 3)
            wind_speed.append((scrapers.value_extract(data2['weather_dep'], '"wind_speed":', ',') +
                               scrapers.value_extract(data2['weather_arr'], '"wind_speed":', ',') * 2) / 3)

            w_notes.append(input('enter notes to add for weather (type "delete" to remove):'))


w_new = pd.DataFrame({'Race': races_labelled})
w_new['temp'] = temp
w_new['feels_like'] = feels_like
w_new['pressure'] = pressure
w_new['humidity'] = humidity
w_new['dew_point'] = dew_point
w_new['clouds'] = clouds
w_new['wind_speed'] = wind_speed
w_new['Note'] = w_notes

w_new = w_new[w_new['Note'] != 'delete']
w_new = pd.concat([w_old, w_new])
