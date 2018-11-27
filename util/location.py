import json, urllib.request

API_LINK = ' https://api.openstreetmap.org/search'

def get_raw_data(location):
    url = API_LINK + 'q=' + location + '&format=json'
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

print(get_raw_data('brooklyn'))
