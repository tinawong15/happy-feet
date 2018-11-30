import os

from flask import Flask, render_template, request, session, redirect, url_for

#from passlib.hash import sha256_crypt
from util import news, fortune, user, forecast, location


app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def home():
    keyword = request.args.get('search', '')
    raw = news.top_headlines_by_keyword(keyword)
    articles = news.list_article_titles(raw)
    links = news.list_article_urls(raw)
    dictionary = {}
    message = ''
    type = 'warning'

    i = 0
    while (i < len(articles)):
        dictionary[articles[i]] = links[i]
        i += 1
    #for debugging
    #print(dictionary)

    quote = fortune.getQuote()
    if 'searchLoc' in request.args:
        # print(request.args['searchLoc'])
        loc = request.args['searchLoc']

    else:
        loc = 'manhattan'

    coordinates = location.get_coordinates(loc)

    if 'username' in session:
        if 'newTag' in request.args:
            if not user.addTag(session['username'], request.args['newTag']):
                message = 'Tag already exists.'

        if 'newLoc' in request.args:
            if not user.addLoc(session['username'], request.args['newLoc']):
                message = 'Location already exists.'

        session['stats'] = user.getStats(session['username'])

    if dictionary:
        data = dictionary
    else:
        data = { 'No results found! Try again' : '/' }

    if 'username' in session:
        return render_template('home.html', m = message, t = type, q = quote[0], c = quote[1], d = data, li = True, u = session['username'], s = session['stats'], l = loc, daily_summary = forecast.get_daily_summary(coordinates[0], coordinates[1]))
    else:
        return render_template('home.html', m = message, t = type, q = quote[0], c = quote[1], d = data, li = False, l = loc, daily_summary = forecast.get_daily_summary(coordinates[0], coordinates[1]))

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
        return redirect('/')
    else:
        message = "Invalid Username Password Combination"
        return render_template('login.html', hm = hasMsg, msg = message, t = type)

@app.route('/logout')
def logout():
    '''This function removes the username from the session, logging the user out. Redirects user to home page.'''
    session.pop('username') # ends session
    return redirect(url_for('home'))

@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
