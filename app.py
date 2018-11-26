# from passlib.hash import sha256_crypt
from util import news, fortune
import os
from flask import Flask, render_template, request, session

app = Flask(__name__)

app.secret_key = os.urandom(32)

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
    return render_template('home.html', hm = False, q = quote[0], c = quote[1], d = data)

@app.route('/signup')
def signup():
    return render_template('signup.html', hasMsg = False)

@app.route('/signupauth', methods = ['POST'])
def signupauth():
    session['username'] = request.form['username']
    session['password0'] = request.form['password0']
    session['password1'] = request.form['password1']
    hasMsg = True
    type = 'alert'
    message = ''
    if len(session['username']) < 5:
        message = "You have entered an invalid username. Please try again."
        return render_template('signup.html', hm = hasMsg, msg = message, t = type)
    elif len(session['password0']) < 5:
        message = "You have entered an invalid password. Please try again."
        return render_template('signup.html', hm = hasMsg, msg = message, t = type)
    elif session['password0'] != session['password1']:
        message = "Passwords do not match. Please try again."
        return render_template('signup.html', hm = hasMsg, msg = message, t = type)
    else:
        return render_template('signupauth.html')

'''@app.route('/login')
def login():
    return render_template('login.html', hasMsg = False)
'''

if __name__ == "__main__":
    app.debug = True
    app.run()
