import os

from flask import Flask, render_template, request, session, redirect, url_for, flash

#from passlib.hash import sha256_crypt
from util import news, fortune, user, forecast, location

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/', methods=['GET'])
def home():
    '''This function renders the template for the homepage and displays the latest news, weather, and a fortune. It also allows logged in users to add tags they would like to see.'''
    keyword = request.args.get('search', '')

    #try-except block added in case the API calls fail
    try:
        raw = news.top_headlines_by_keyword(keyword)
        articles = news.list_article_titles(raw)
        links = news.list_article_urls(raw)
        dictionary = {}
    except:
        raw = {"Error pulling articles from API - possible API key error!" : ""}
        dictionary = {"Error pulling articles from API - possible API key error!" : ""}
        articles = {}
        links = {}

    message = ''
    type = ''

    if 'message' in session:
        message = session['message']
        type = 'success'
        session.pop('message')


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
    # if 'searchLoc' in request.args and request.args['searchLoc'] != '':
    #     # print(request.args['searchLoc'])
    #     session['location'] = request.args['searchLoc']
    #
    # elif 'location' not in session:
    #     session['location'] = 'Manhattan'
    #
    # print(session['location'])
    # coordinates = location.get_coordinates(session['location'])
    #
    # forecast_data = forecast.get_json(coordinates[0], coordinates[1])

    if 'username' in session:
        if 'newTag' in request.args:
            if request.args['newTag'] == '':
                message = 'Tag cannot be empty.'
                type = 'alert'
            else:
                if not user.addTag(session['username'], request.args['newTag']):
                    message = 'Error: Tag already exists.'
                    type = 'alert'

        if 'newLoc' in request.args:
            if request.args['newLoc'] == '':
                message = 'Location cannot be empty.'
                type = 'alert'
            else:
                if not user.addLoc(session['username'], request.args['newLoc']):
                    message = 'Error: Location already exists.'
                    type = 'alert'

        session['stats'] = user.getStats(session['username'])

    forecast_dict = {}
    loc = []

    if 'searchLoc' in request.args and request.args['searchLoc'] != '':
        loc.append(request.args['searchLoc'])

    elif 'username' not in session or session['stats']['locations'] == []:
        loc.append('New York')

        #coordinates = location.get_coordinates(loc)
        #datum = forecast.get_json( coordinates[0], coordinates[1] )
        #forecast_dict[loc] = forecast.get_daily_summary(datum)
    else:
        for l in session['stats']['locations']:
            loc.append(l)
            # print('[' + loc + ']')

    #for each location in the user's database, loop thru and get info for it
    #if there are any errors, prints such
    for l in loc:
        try:
        #     if l == 'ERROR':
        #         forecast_dict[l] = 'Invalid location! No results found!'
            coordinates = location.get_coordinates(l)
            datum = forecast.get_json( coordinates[0], coordinates[1] )
            forecast_dict[l] = forecast.get_daily_summary(datum)
        # forecast_dict['name'] = location.get_name(l)
        except:
            forecast_dict[l] = "API ERROR for the DARK SKY API\nEither the API key is invalid or you put in an invalid location"
    if dictionary:
        data = dictionary
    else:
        data = { 'No results found! Try again' : '/' }

    if 'username' in session:
        #print(forecast_dict)
        return render_template('home.html', m = message, k = keyword, t = type, q = quote[0], c = quote[1], d = data, li = True, u = session['username'], s = session['stats'], fd = forecast_dict)
    else:
        #print(forecast_dict)
        return render_template('home.html', m = message, k = keyword, t = type, q = quote[0], c = quote[1], d = data, li = False, fd = forecast_dict)

@app.route('/signup')
def signup():
    '''This function renders the HTML template for the signup page.'''
    return render_template('signup.html', m = '')

@app.route('/signupauth', methods = ['POST'])
def signupauth():
    '''This function checks the form on the signup page and calls register() to register the user into the database.'''
    usern = request.form['username']
    pswd0 = request.form['password0']
    pswd1 = request.form['password1']
    q = request.form['question']
    a = request.form['answer']

    hasMsg = True
    type = 'alert'
    message = ''
    fail = True

    numbers = '0123456789'

    if len(usern) < 5:
        message = "Username is too short. Please try again."
    elif len(pswd0) < 5:
        message = "Password is too short. Please try again."
    elif pswd0 != pswd1:
        message = "Passwords do not match. Please try again."
    elif q == '':
        message = "Please don't leave the question blank."
    elif a == '':
        message = "Please don't leave the answer blank."
    elif numbers.find(usern[: 1]) != -1:
        message = "The first character of username must be a letter."
    else:
        user.register(usern, pswd0, request.form['question'], request.form['answer'])
        session['message'] = 'You have successfully signed up.'
        fail = False
    if fail:
        return render_template('signup.html', m = message, t = type)
    return redirect('/')

@app.route('/login')
def login():
    '''This function renders the HTML template for the login page.'''
    return render_template('login.html', m = '')

@app.route('/loginauth', methods = ['POST'])
def loginauth():
    '''This function calls authenticate() to check if the form's username and password match the database. If successful, this function redirects the user to the home page.'''
    username = request.form['username']
    password = request.form['password']
    type = 'alert'
    message = ''
    if user.authenticate(username, password):
        session['username'] = username
        session['stats'] = user.getStats(username)
        session['message'] = 'You have successfully logged in.'
        return redirect('/')
    else:
        message = "Invalid Username Password Combination"
        return render_template('login.html', m = message, t = type)

@app.route('/logout')
def logout():
    '''This function removes the username from the session, logging the user out. Redirects user to home page.'''
    session.pop('username') # ends session
    session['message'] = 'You have successfully logged out.'
    return redirect('/')

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    '''This function handles removing the user's tags and specified location and calls resetPassword() to allow the user to change their password through the form displayed.'''
    message = ''
    type = ''
    if 'username' in session:
        if 'oldPass' in request.form:
            if user.authenticate(session['username'], request.form['oldPass']):
                if len(request.form['newPass0']) < 5:
                    message = 'New password is too short.'
                    type = 'alert'
                elif request.form['newPass0'] != request.form['newPass1']:
                    message = 'New passwords do not match.'
                    type = 'alert'
                else:
                    user.resetPassword(session['username'], request.form['newPass0'])
                    message = 'Your have successfully reset your password'
                    type = 'success'
            else:
                message = 'Reset failed: Invalid Username Password Combination'
                type = 'alert'

        if 'rmTag' in request.args:
            # request.args.pop('rmTag')
            for tag in request.args:
                if tag != 'rmTag':
                    user.removeTag(session['username'], tag)
                    message = 'Tags are successfully removed.'
                    type = 'success'

        if 'rmLoc' in request.args:
            # request.args.pop('rmLoc')
            for loc in request.args:
                if loc != 'rmLoc':
                    user.removeLoc(session['username'], loc)
                    message = 'Locations are successfully removed.'
                    type = 'success'
        session['stats'] = user.getStats(session['username'])
        return render_template("settings.html", li = True, m = message, t = type, s = session['stats'])
    else:
        flash("You must be logged in to see that page.")
        return redirect(url_for('login'))

@app.route("/weather/<lo>", methods = ['GET', 'POST'])
def weather(lo):
    if 'message' in session:
        message = session['message']
        type = 'success'
        session.pop('message')
    else:
        message = ''
        type = ''

    forecast_dict = {}
    loc = []

    if 'searchLoc' in request.args and request.args['searchLoc'] != '':
        loc.append(request.args['searchLoc'])

    elif 'username' not in session or session['stats']['locations'] == []:
        loc.append('New York')
        #coordinates = location.get_coordinates(loc)
        #datum = forecast.get_json( coordinates[0], coordinates[1] )
        #forecast_dict[loc] = forecast.get_daily_summary(datum)
    else:
        loc.append(lo)
            # print('[' + loc + ']')

    #for each location in the user's database, loop thru and get info for it
    #if there are any errors, prints such
    try:
        for l in loc:
            coordinates = location.get_coordinates(l)
            datum = forecast.get_json( coordinates[0], coordinates[1] )
            forecast_dict[l] = forecast.get_daily_summary(datum)

        coor = location.get_coordinates(lo)
        data = forecast.get_json( coor[0], coor[1] )

        ds = forecast.get_daily_summary(data)
        ct = forecast.get_temp(data)
        at = forecast.get_apparent_temp(data)

        fds = []
        fdt = []
        fdat = []
        fdpc = []
        fdpt = []
        i = 1
        while(i < 8):
            fds.append(forecast.get_future_daily_summary(data, i))
            fdt.append(forecast.get_future_daily_temp_high(data, i))
            fdat.append(forecast.get_future_daily_temp_low(data, i))
            fdpc.append(forecast.get_future_daily_precipitation_chance(data, i))
            fdpt.append(forecast.get_future_daily_precipitation_type(data, i))
            i += 1
    except:
        flash("API ERROR for the DARK SKY API. Either the API key is invalid or you put in an invalid location.")
        return redirect('/')

    if 'username' in session:
        return render_template('weather.html', li=True, lo = lo, m = message, t = type,  fd = forecast_dict, ct = ct, at = at, ds = ds, fds = fds, fdt = fdt, fdat = fdat, fdpc = fdpc, fdpt = fdpt)
    else:
        return render_template('weather.html', li=False, lo = lo, m = message, t = type,  fd = forecast_dict, ct = ct, at = at, ds = ds, fds = fds, fdt = fdt, fdat = fdat, fdpc = fdpc, fdpt = fdpt)

@app.route('/forgetpass')
def forgetpass():
    '''This function renders the template for the forget password form.'''
    return render_template('forgetpass.html', m = '')

@app.route('/resetpass', methods = ['POST'])
def resetpass():
    '''This function resets the password by requesting the user's security question and answer.'''
    session['username'] = request.form['username']
    session['stats'] = user.getStats(session['username'])
    # session['question'] = user.getQuestion(session['usr'])
    message = ''
    type = ''
    if session['stats'] == -1:
        message = 'Username does not exist.'
        type = 'alert'
        session.pop('username')
        session.pop('stats')
        return render_template('forgetpass.html', m = message, t = type)
    return render_template('resetpass.html', m = message, t = type, q = session['stats']['question'])

@app.route('/resetauth', methods = ['POST'])
def resetauth():
    '''This function uses the user's responses in the form to reset the password.'''
    if session['stats']['answer'] == request.form['answer']:
        if len( request.form['password0'] ) < 5:
            message = 'Password is too short. Please try again.'
            type = 'alert'
        if request.form['password0'] == request.form['password1']:
            user.resetPassword(session['username'], request.form['password0'])
            session['message'] = 'Your password is successfully reset.'
            session.pop('username')
            session.pop('stats')
            return redirect('/')
        else:
            message = 'Passwords do not match.'
            type = 'alert'
    else:
        message = 'Invalid Answer'
        type = 'alert'
    return render_template('resetpass.html', m = message, t = type, q = session['stats']['question'])

if __name__ == "__main__":
    app.debug = True
    app.run()
