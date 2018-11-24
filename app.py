# from passlib.hash import sha256_crypt
from util import news, fortune

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    keyword = request.args.get('search', '')

    raw = news.top_headlines_by_keyword(keyword)
    articles = news.list_article_titles(raw)
    links = news.list_article_urls(raw)
    dictionary = {}

    i = 0
    while (i < len(articles)):
        dictionary[articles[i]] = links[i]
        i += 1
    #for debugging
    #print(dictionary)
    quote = fortune.getQuote()
    if dictionary:
        data = dictionary
    else:
        data = { 'No results found! Try again' : '/' }
    return render_template('home.html', q = quote[0], c = quote[1], d = data)

if __name__ == "__main__":
    app.debug = True
    app.run();
