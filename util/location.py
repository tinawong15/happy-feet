import json, urllib.request

API_LINK = 'http://dev.virtualearth.net/REST/v1/Locations?query='
API_KEY = 'AiIs8nS3kIqOkEJUD9uKnIpk4WecoekWcF39HhFxfaCutK2c652aCU5nqwAaeWFf'

def get_raw_data(location):
    url = API_LINK + location + '&key=' + API_KEY
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def get_coordinates(location):
    data = get_raw_data(location)
    return data['resourceSets'][0]['resources'][0]['point']['coordinates']
    

#print(get_raw_data('brooklyn'))
print(get_coordinates('brooklyn'))
