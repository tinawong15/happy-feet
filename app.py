# from passlib.hash import sha256_crypt
from util import news, fortune, user
import os
from flask import Flask, render_template, request, session, redirect

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
    if 'username' in session:
        return render_template('home.html', hm = False, q = quote[0], c = quote[1], d = data, li = True, u = session['username'], s = session['stats'])
    else:
        return render_template('home.html', hm = False, q = quote[0], c = quote[1], d = data, li = False)

@app.route('/signup')
def signup():
    return render_template('signup.html', hasMsg = False)

@app.route('/signupauth', methods = ['POST'])
def signupauth():
    usern = request.form['username']
    pswd0 = request.form['password0']
    pswd1 = request.form['password1']
    hasMsg = True
    type = 'alert'
    message = ''
    if len(usern) < 5:
        message = "You have entered an invalid username. Please try again."
        return render_template('signup.html', hm = hasMsg, msg = message, t = type)
    elif len(pswd0) < 5:
        message = "You have entered an invalid password. Please try again."
        return render_template('signup.html', hm = hasMsg, msg = message, t = type)
    elif pswd0 != pswd1:
        message = "Passwords do not match. Please try again."
        return render_template('signup.html', hm = hasMsg, msg = message, t = type)
    else:
        user.register(usern, pswd0, request.form['question'], request.form['answer'])
        return render_template('signupauth.html')

@app.route('/login')
def login():
    return render_template('login.html', hasMsg = False)

@app.route('/loginauth', methods = ['POST'])
def loginauth():
    username = request.form['username']
    password = request.form['password']
    hasMsg = True
    type = 'alert'
    message = ''
    if user.authenticate(username, password):
        session['username'] = username
        session['stats'] = user.getStats(username)
        return redirect('/')
    else:
        message = "Invalid Username Password Combination"
        return render_template('login.html', hm = hasMsg, msg = message, t = type)


if __name__ == "__main__":
    app.debug = True
    app.run()
