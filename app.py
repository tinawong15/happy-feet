from passlib.hash import sha256_crypt
from util import news

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    raw = news.top_headlines_by_keyword('bitcoin')
    articles = news.list_article_titles(raw)
    links = news.list_article_urls(raw)
    dictionary = {}

    i = 0
    while (i < len(articles)):
        dictionary[articles[i]] = links[i]
        i += 1
    
    print(dictionary)

    return render_template('home.html', data = dictionary) 
