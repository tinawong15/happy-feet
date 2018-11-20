from flask import Flask
from passlib.hash import sha256_crypt

app = Flask(__name__)

@app.route('/')
def home():
    return "<center><h1> UwU News </h1></center>"
