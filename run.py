from flask import Flask, redirect, url_for, render_template, request, session, flash, make_response, \
    render_template_string
from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv
from datetime import datetime as dt
from jinja2 import Environment
import dns

app = Flask(__name__, template_folder='./app/templates', static_folder='./app/static')

# .env necessary to connect to MongoDB
load_dotenv()
MONGO_USER = environ.get("MONGO_USER")
MONGO_PASSWORD = environ.get("MONGO_PASSWORD")


# Connect to Mongo. Will likely put in db folder or __init__.py
def connect_mongo():
    db_client = MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.kxem4.mongodb.net/safetravels"
                            f"?retryWrites=true&w=majority")
    db = db_client.safetravels
    return db


# Initial route to home
@app.route('/')
def hello_flask():
    return '''
    <html>
        <head>
            <title>Hello Flask!</title>
        </head>
        <body>
            <h1>Welcome to safetravels!</h1>
            <p>We hope you like the website.</p>
            <p><a href="%s">Go to index template</a></p>
            <p><a href="%s">Go to mongo example</a></p>
        </body>
    </html>''' % (url_for('index'), url_for('hello_mongo'))


# Example of using MongoDB
@app.route('/mongo')
def hello_mongo():
    db = connect_mongo()
    collection = db['safetravels-collection']
    result = collection.find({"string": {"$exists": True}})
    for doc in result:
        return str(doc.get("string"))


# Example of templating
@app.route('/index')
def index():
    message = "Hello from my template! The time is: " + str(dt.now())
    image = url_for('static', filename='images/logo.png')
    return render_template('index.html', message=message, image=image)
