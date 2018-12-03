# happy-feet
### Vincent Lin, William Lu, Rubin Peci, Tina Wong

P01: ArRESTed Development

## Description
UwU News is a website that displays the latest news articles, weather forecasts of a location, and a quote/fact of the day by using the News API, Bing Maps API, Dark Sky API, and Fortune Cookie API. This will serve as a home page for the user. If logged in, the articles and forecast shown will be based on the user's preferences when they make their account and can be changed whenever they please.

## Instructions to Run
1. Clone this repository:
```
$ git clone git@github.com:tinawong15/happy-feet.git
```

2. Change your directory to go into your local copy of the repository:
```
$ cd happy-feet
```

3. Activate your virtual environment. If you do not have one set up, you may create one in the current working directory, and activate it like so:
```
$ python3 -m venv venv
$ . venv/bin/activate
```

4. In your virtual environment, install the dependencies:
```
(venv) $ pip install -r requirements.txt
```

5. Now, run the python file to start the Flask server:
```
(venv) $ python app.py
```

6. Open your web browser and open `localhost:5000`.

7. To terminate your server instance, type <kbd> CTRL </kbd> + <kbd> C </kbd>.

8. To deactivate your virtual environment, type `deactivate`.

## Dependencies
- News API
     - Procure an API key [here](https://newsapi.org/). After clicking on "Get API key" to register, an API key will be presented.
     - Use API key to request information from API.
     - The API retrieves articles from over 30,000 news sources and blogs and returns it as a JSON.
     - We used this API to request the latest headlines and the links to the actual articles to display on the home page of our site. We also used its search capability to display relevant news articles based on the user's query.
- Dark Sky API
     - Procure an API key [here](https://darksky.net/dev) by registering your email. Click the link to verify your identity.
     - Login and request a key.
     - Use API key to request information from API about the current and future weather.
     - The API retrieves weather alerts, forecasts and current conditions, historical data, and global weather coverage and returns it as a JSON.
- Bing Maps API
     - Procure an API key [here](https://www.bingmapsportal.com/) by registering for a Microsoft account.
     - Use API key to request information from API.
     - The API provides access to geospatial features such as geocoding, route and traffic data and spatial data sources.
     - We used this API to request the location of the user. We combined this information with the Dark Sky API to provide the user with accurate weather based on the location that the user is from.
- Fortune Cookie API
     - no API key needed, but documentation is [here](http://yerkee.com/api/).
     - The API retrieves a random fortune cookie from any category and returns it as a JSON.
     - We used this API to request a random quote and the author of the quote to display on the home page of our site.  
