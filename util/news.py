import json, urllib.request

API_LINK = 'https://newsapi.org/v2/top-headlines?'
API_KEY = "a842f08935ec4c4f8cbfa0ca729fc2c1"

def top_headlines_by_src(src):
    url = ('https://newsapi.org/v2/top-headlines?'
       'sources=' + src + '&'
       'language=en&'
       'apiKey=' + API_KEY)
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def top_headlines_by_keyword(keyword):
    url = ('https://newsapi.org/v2/top-headlines?'
        'q=' + keyword + '&'
        'sortBy=popularity&'
        'language=en&'
       'apiKey=' + API_KEY)
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

#debug print statements
#print(top_headlines_by_keyword('Apple'))
