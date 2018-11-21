from passlib.hash import sha256_crypt
from util import news

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    articles = news.list_article_titles(news.top_headlines_by_keyword('bitcoin'))
    return render_template('home.html', list = articles) 
