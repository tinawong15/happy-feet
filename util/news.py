import json, urllib.request

API_LINK = 'https://newsapi.org/v2/top-headlines?'
API_KEY = "a842f08935ec4c4f8cbfa0ca729fc2c1"

#gets raw json data of top headlines by source
def top_headlines_by_src(src):
    url = ('https://newsapi.org/v2/top-headlines?'
       'sources=' + src + '&'
       'language=en&'
       'apiKey=' + API_KEY)
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

#gets raw json data of top headlines by keyword
def top_headlines_by_keyword(keyword):
    url = ('https://newsapi.org/v2/top-headlines?'
        'q=' + keyword + '&'
        'sortBy=popularity&'
        'language=en&'
       'apiKey=' + API_KEY)
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

#returns a list of article titles based off of raw json data
def list_article_titles(raw_json):
    ret_list = []

    for article in raw_json['articles']:
        if article['title'] == None:
            ret_list.append('No title')
        else:
            ret_list.append(article['title'])

    return ret_list

#returns a list of article authors based off of raw json data
def list_article_authors(raw_json):
    ret_list = []

    for article in raw_json['articles']:
        if article['author'] == None:
            ret_list.append('No Author')
        else:
            ret_list.append(article['author'])

    return ret_list

#returns a list of article descriptions based off of raw json data
def list_article_desc(raw_json):
    ret_list = []

    for article in raw_json['articles']:
        if article['description'] == None:
            ret_list.append('')
        else:
            ret_list.append(article['description'])
    return ret_list

#returns a list of article urls based off of raw json data
def list_article_urls(raw_json):
    ret_list = []

    for article in raw_json['articles']:
        if article['url'] == None:
            ret_list.append('')
        else:
            ret_list.append(article['url'])
    return ret_list

#returns a list of article img urls based off of raw json data
def list_article_imgs(raw_json):
    ret_list = []

    for article in raw_json['articles']:
        if article['urlToImage'] == None:
            ret_list.append('')
        else:
            ret_list.append(article['urlToImage'])
    return ret_list


#debug print statements
#print(top_headlines_by_keyword('bitcoin'))
#print(list_article_titles(top_headlines_by_keyword('bitcoin')))
#print(list_article_titles(top_headlines_by_src('bbc-news')))
#print(list_article_authors(top_headlines_by_keyword('bitcoin')))
#print(list_article_desc(top_headlines_by_keyword('bitcoin')))
#print(list_article_urls(top_headlines_by_keyword('bitcoin')))
#print(list_article_imgs(top_headlines_by_keyword('bitcoin')))


