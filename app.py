from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<center><h1> UwU News </h1></center>"
