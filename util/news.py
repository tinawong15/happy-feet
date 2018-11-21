import json, urllib.request

API_LINK = 'https://newsapi.org/v2/top-headlines?'
API_KEY = "a842f08935ec4c4f8cbfa0ca729fc2c1"

def top_headlines_by_src(src):
    url = ('https://newsapi.org/v2/top-headlines?'
       'sources=' + src + '&'
       'apiKey=' + API_KEY)
    response = requests.get(url)
    return json.loads(response.text)

def top_headlines_by_keyword(keyword):
