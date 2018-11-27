import json, urllib.request, time

API_LINK = 'https://api.darksky.net/forecast/'
API_KEY = '65661444800d8180135cd4c62317a82c'

def get_json(lat, lon):
    response = urllib.request.urlopen(API_LINK + API_KEY + '/' + str(lat) + ',' + str(lon))
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

def get_weekly_summary(lat, lon):
    data = get_json(lat, lon)
    return data['daily']['summary']

#future requests
def get_next_day(lat, lon):
   return 0 

#print(get_temp(42.3601,-71.0589))
#print(get_minutely_summary(42.3601,-71.0589))
#print(get_weekly_summary(42.3601,-71.0589))
#print(get_hourly_summary(42.3601,-71.0589))
