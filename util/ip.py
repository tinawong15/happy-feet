import urllib.request, json

API_LINK = 'http://api.ipstack.com/'
API_KEY = 'd208269d44db40b5b08e5e39bb4d70f7'

def get_json(ip_address):
    response = urllib.request.urlopen(API_LINK + ip_address + '?access_key=' + API_KEY)
    data = json.loads(response.read())
    return data

def get_location(ip_address):
    data = get_json(ip_address)
    return [data['latitude'], data['longitude']]

#print(get_location("174.202.6.0"))
