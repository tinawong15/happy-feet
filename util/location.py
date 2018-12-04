import json
import urllib.request

API_LINK = 'http://dev.virtualearth.net/REST/v1/Locations?query='
with open('data/keys.json', 'r') as f:
    api_dict = json.load(f)

API_KEY = api_dict["BING_MAPS_API"]

def get_raw_data(location):
    '''This function gets the raw json data based of a search query'''
    url = API_LINK + location + '&key=' + API_KEY
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def get_coordinates(location):
    '''This function gets the coordinates based off a location search (uses the first result)'''
    data = get_raw_data(location)
    return data['resourceSets'][0]['resources'][0]['point']['coordinates']


#print(get_raw_data('brooklyn'))
#print(get_coordinates('brooklyn'))
