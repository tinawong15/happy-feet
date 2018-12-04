import json
import urllib.request
#import location

API_LINK = 'https://api.darksky.net/forecast/'
with open('data/keys.json', 'r') as f:
    api_dict = json.load(f)

API_KEY = api_dict["DARK_SKY_API"]

def get_json(lat, lon):
    '''This function gets json data based off location'''
    response = urllib.request.urlopen(API_LINK + API_KEY + '/' + str(lat) + ',' + str(lon))
    data = json.loads(response.read())
    return data

def get_json_time(lat, lon, date):
    '''This function gets json data based off time and location'''
    response = urllib.request.urlopen(API_LINK + API_KEY + '/' + str(lat) + ',' + str(lon) + ',' + str(date))
    data = json.loads(response.read())
    return data

def get_temp(data):
    '''This function utilizes the 'currently' dictionary, getting most up-to-date data about temperature'''
    return data['currently']['temperature']

def get_apparent_temp(data):
    '''This function utilizes the 'currently' dictionary, getting most up-to-date data about apparent temperature'''
    return data['currently']['apparentTemperature']

def get_minutely_summary(data):
    '''This function gets weather summary based on the minute'''
    return data['minutely']['summary']

def get_hourly_summary(data):
    '''This function gets weather summary based on the hour'''
    return data['hourly']['summary']

def get_daily_summary(data):
    '''This function gets weather summary based on the day'''
    return data['daily']['summary']

def get_current_icon(data):
    '''This function gets the icon for the current time'''
    return data['currently']['icon']

#different way(?) of getting future requests
#hours < 49
def get_future_hourly_summary(data, hours):
    '''This function gets future weather summary on an hour-by-hour basis'''
    return data['hourly']['data'][hours]['summary']

def get_future_hourly_temp(data, hours):
    '''This function gets future temperature on an hour-by-hour basis'''
    return data['hourly']['data'][hours]['temperature']

def get_future_hourly_apparent_temp(data, hours):
    '''This function gets future apparent temperature on an hour-by-hour basis'''
    return data['hourly']['data'][hours]['apparentTemperature']

def get_future_hourly_icon(data, hours):
    '''This function gets future icon on an hour-by-hour basis'''
    return data['hourly']['data'][hours]['icon']

def get_future_hourly_preciptiation_chance(data, hours):
    '''This function gets future precipitation chance on an hour-by-hour basis'''
    return data['hourly']['data'][hours]['precipProbability'] * 100

def get_future_hourly_precipitation_type(data, hours):
    '''This function gets future precipitation type on an hour-by-hour basis'''
    return data['hourly']['data'][hours]['precipType']

def get_future_hourly_UV_index(data, hours):
    '''This function gets future UV index on an hour-by-hour basis'''
    return data['hourly']['data'][hours]['uvIndex']

#days < 8
def get_future_daily_summary(data, days):
    '''This function gets future daily weather summary for 7 days'''
    return data['daily']['data'][days]['summary']

def get_future_daily_temp(data, days):
    '''This function gets future daily temperature for up to 7 days'''
    return data['daily']['data'][days]['temperature']

def get_future_daily_apparent_temp(data, days):
    '''This function gets future daily apparent temperature for up to 7 days'''
    return data['daily']['data'][days]['apparentTemperature']

def get_future_daily_icon(data, days):
    '''This function gets the future daily icon for up to 7 days'''
    return data['daily']['data'][days]['icon']

def get_future_daily_preciptiation_chance(data, days):
    '''This function gets the future daily precipitation chance for up to 7 days'''
    return data['daily']['data'][days]['precipProbability']

def get_future_daily_precipitation_type(data, days):
    '''This function gets the future daily precipitation type for up to 7 days'''
    return data['daily']['data'][days]['precipType']

def get_future_daily_UV_index(data, days):
    '''This function gets the future daily UV type for up to 7 days'''
    return data['daily']['data'][days]['uvIndex']

def get_future_daily_sunrise(data, days):
    '''This function gets the future daily sunrise time for up to 7 days'''
    return data['daily']['data'][days]['sunriseTime']

def get_future_daily_sunset(data, days):
    '''This function gets the future daily sunset time for up to 7 days'''
    return data['daily']['data'][days]['sunsetTime']


#print(get_temp(42.3601,-71.0589))
#print(get_minutely_summary(42.3601,-71.0589))
#print(get_daily_summary(42.3601,-71.0589))
#print(get_hourly_summary(42.3601,-71.0589))
#print(get_future_summary(42.3601,-71.0589, 1))
#print(get_future_summary(42.3601,-71.0589, 2))
#print(get_future_summary(42.3601,-71.0589, 3))

'''
print(get_future_hourly_summary(42.3601,-71.0589, 1))
print(get_future_hourly_summary(42.3601,-71.0589, 2))
print(get_future_hourly_summary(42.3601,-71.0589, 3))
print(get_future_hourly_summary(42.3601,-71.0589, 4))
print(get_future_hourly_summary(42.3601,-71.0589, 5))
print(get_future_hourly_summary(42.3601,-71.0589, 6))
print(get_future_hourly_summary(42.3601,-71.0589, 7))

print(get_future_daily_summary(42.3601,-71.0589, 1))
print(get_future_daily_summary(42.3601,-71.0589, 2))
print(get_future_daily_summary(42.3601,-71.0589, 3))
print(get_future_daily_summary(42.3601,-71.0589, 4))
print(get_future_daily_summary(42.3601,-71.0589, 5))
print(get_future_daily_summary(42.3601,-71.0589, 6))
print(get_future_daily_summary(42.3601,-71.0589, 7))
print(get_future_daily_summary(42.3601,-71.0589, 8))
'''

'''
testing implimentation of location.py
works as intended!

test = location.get_coordinates('brooklyn')
print(get_daily_summary(test[0], test[1]))
'''
