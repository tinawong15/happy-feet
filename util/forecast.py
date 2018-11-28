import json, urllib.request
#import ip
API_LINK = 'https://api.darksky.net/forecast/'
API_KEY = '65661444800d8180135cd4c62317a82c'

#get json data based off location
def get_json(lat, lon):
    response = urllib.request.urlopen(API_LINK + API_KEY + '/' + str(lat) + ',' + str(lon))
    data = json.loads(response.read())
    return data

#get json data based off time and location
def get_json_time(lat, lon, date):
    response = urllib.request.urlopen(API_LINK + API_KEY + '/' + str(lat) + ',' + str(lon) + ',' + str(date))
    data = json.loads(response.read())
    return data

#utilizing the 'currently' dictionary, getting most up-to-date data
def get_temp(lat, lon):
    data = get_json(lat, lon)
    return data['currently']['temperature']

def get_apparent_temp(lat, lon):
    data = get_json(lat, lon)
    return data['currently']['apparentTemperature']

#getting summaries based on timeframe
def get_minutely_summary(lat, lon):
    data = get_json(lat, lon)
    return data['minutely']['summary']

def get_hourly_summary(lat, lon):
    data = get_json(lat, lon)
    return data['hourly']['summary']

def get_daily_summary(lat, lon):
    data = get_json(lat, lon)
    return data['daily']['summary']


#different way(?) of getting future requests
#hours < 49 
def get_future_hourly_summary(lat, lon, hours):
    data = get_json(lat, lon)
    return data['hourly']['data'][hours]['summary']

def get_future_hourly_temp(lat, lon, hours):
    data = get_json(lat, lon)
    return data['hourly']['data'][hours]['temperature']

def get_future_hourly_apparent_temp(lat, lon, hours):
    data = get_json(lat, lon)
    return data['hourly']['data'][hours]['apparentTemperature']

#days < 8
def get_future_daily_summary(lat, lon, days):
    data = get_json(lat, lon)
    return data['daily']['data'][days]['summary']

def get_future_daily_temp(lat, lon, days):
    data = get_json(lat, lon)
    return data['daily']['data'][days]['temperature']

def get_future_daily_apparent_temp(lat, lon, days):
    data = get_json(lat, lon)
    return data['daily']['data'][days]['apparentTemperature']

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
testing implimentation of ip.py
works as intended!

test = ip.get_location("174.202.6.0")
print(get_daily_summary(test[0], test[1]))
'''
