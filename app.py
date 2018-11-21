from passlib.hash import sha256_crypt
from util import news

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<center><h1> UwU News </h1></center>"
