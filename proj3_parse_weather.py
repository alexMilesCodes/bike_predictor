import pandas as pd


# define a function that takes in:
#    tem - alias of temp
#    start - string indicating the start of the stat string
#    fin - string indicating the end of the stat string
#    cut - if true, return tem but with the string and everything before removed
# ...and returns the extracted string
def value_extract(tem, start, fin, cut=False):
    te = tem
    da = tem.find(start)
    if da >= 0:
        da += len(start)
        te = tem[da:]
        output = te[:te.find(fin)]
    else:
        output = ''
    if cut:
        return output, te
    else:
        return output


data = pd.read_csv('Book5.csv')

for loc in ['dep', 'arr']:

    temp = []
    feels_like = []
    pressure = []
    humidity = []
    dew_point = []
    clouds = []
    visibility = []
    wind_speed = []
    wind_deg = []
    main = []
    desc = []
    for i in data.index:
        temp.append(value_extract(data['weather_'+loc][i], '"temp":', ','))
        feels_like.append(value_extract(data['weather_'+loc][i], '"feels_like":', ','))
        pressure.append(value_extract(data['weather_'+loc][i], '"pressure":', ','))
        humidity.append(value_extract(data['weather_'+loc][i], '"humidity":', ','))
        dew_point.append(value_extract(data['weather_'+loc][i], '"dew_point":', ','))
        clouds.append(value_extract(data['weather_'+loc][i], '"clouds":', ','))
        visibility.append(value_extract(data['weather_'+loc][i], '"visibility":', ','))
        wind_speed.append(value_extract(data['weather_'+loc][i], '"wind_speed":', ','))
        wind_deg.append(value_extract(data['weather_'+loc][i], '"wind_deg":', ','))
        main.append(value_extract(data['weather_'+loc][i], '"main":"', '",'))
        desc.append(value_extract(data['weather_'+loc][i], '"description":"', '",'))

    data['temp_'+loc] = temp
    data['feels_like_'+loc] = feels_like
    data['pressure_'+loc] = pressure
    data['humidity_'+loc] = humidity
    data['dew_point_'+loc] = dew_point
    data['clouds_'+loc] = clouds
    data['visibility_'+loc] = visibility
    data['wind_speed_'+loc] = wind_speed
    data['wind_deg_'+loc] = wind_deg
    data['main_'+loc] = main
    data['desc_'+loc] = desc

data.to_csv('Book1.csv', index=False)
