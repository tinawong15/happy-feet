import os

from flask import Flask, render_template, request, session, redirect, url_for

#from passlib.hash import sha256_crypt
from util import news, fortune, user, forecast, location

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/', methods=['GET'])
def home():
    keyword = request.args.get('search', '')
    raw = news.top_headlines_by_keyword(keyword)
    articles = news.list_article_titles(raw)
    links = news.list_article_urls(raw)
    dictionary = {}

    if 'message' in session:
        message = session['message']
        type = 'success'
        session.pop('message')
    else:
        message = ''
        type = ''

    if keyword != '':
        message = 'New Search Keyword: '
        type = 'success'

    i = 0
    while (i < len(articles)):
        dictionary[articles[i]] = links[i]
        i += 1
    #for debugging
    #print(dictionary)

    quote = fortune.getQuote()
    if 'searchLoc' in request.args and request.args['searchLoc'] != '':
        # print(request.args['searchLoc'])
        session['location'] = request.args['searchLoc']

    elif 'location' not in session:
        session['location'] = 'Manhattan'

    print(session['location'])
    coordinates = location.get_coordinates(session['location'])

    forecast_data = forecast.get_json(coordinates[0], coordinates[1])

    if 'username' in session:
        if 'newTag' in request.args:
            if not user.addTag(session['username'], request.args['newTag']):
                message = 'Error: Tag already exists.'
                type = 'warning'

        if 'newLoc' in request.args:
            if not user.addLoc(session['username'], request.args['newLoc']):
                message = 'Error: Location already exists.'
                type = 'warning'

        session['stats'] = user.getStats(session['username'])

    if dictionary:
        data = dictionary
    else:
        data = { 'No results found! Try again' : '/' }

    if 'username' in session:
        return render_template('home.html', m = message, k = keyword, t = type, q = quote[0], c = quote[1], d = data, li = True, u = session['username'], s = session['stats'], l = session['location'], daily_summary = forecast.get_daily_summary(forecast_data))
    else:
        return render_template('home.html', m = message, k = keyword, t = type, q = quote[0], c = quote[1], d = data, li = False, l = session['location'], daily_summary = forecast.get_daily_summary(forecast_data))

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
        session['message'] = 'You have successfully signed up.'
        return redirect('/')

@app.route('/login')
def login():
    message = ''
    return render_template('login.html', msg = message)

@app.route('/loginauth', methods = ['POST'])
def loginauth():
    username = request.form['username']
    password = request.form['password']
    type = 'alert'
    message = ''
    if user.authenticate(username, password):
        session['username'] = username
        session['message'] = 'You have successfully logged in.'
        return redirect('/')
    else:
        message = "Invalid Username Password Combination"
        return render_template('login.html', msg = message, t = type)

@app.route('/logout')
def logout():
    '''This function removes the username from the session, logging the user out. Redirects user to home page.'''
    session.pop('username') # ends session
    session.pop('location')
    session['message'] = 'You have successfully logged out.'
    return redirect('/')

@app.route("/settings")
def settings():
    message = ''
    return render_template("settings.html", li = True, msg = message, s = session['stats'])


if __name__ == "__main__":
    app.debug = True
    app.run()
