from flask import Flask, redirect, url_for, render_template, request, session, flash, make_response, \
    render_template_string
from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv
from datetime import datetime as dt
from jinja2 import Environment
import dns, requests

app = Flask(__name__, template_folder='./app/templates', static_folder='./app/static')
app.config['SECRET_KEY'] = 'I figure if I study high, take the test high, get high scores! Right?'

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
@app.route('/', methods=['GET', 'POST'])
def hello_flask():
    if request.method == 'POST':
        text = request.form.get('search')
        if len(text) < 1:
            flash('Flash Message Test', category="error")
    return render_template('home.html')


# Example of using MongoDB
@app.route('/mongo')
def hello_mongo():
    db = connect_mongo()
    collection = db['safetravels-collection']
    result = collection.find({"string": {"$exists": True}})
    for doc in result:
        return str(doc.get("string"))


# Search page, not yet integrated with the JS search bar
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        req = request.form
        state = req.get("state").lower()  
        if state in us_state_abbrev:
            abbrev = us_state_abbrev.get(state)      
            return redirect(f"/us/{state}-{abbrev}")
    return render_template("search.html")

def api_handler():
    covid_api = 'ad85ef1a0e9b4ad4aecc0ffe0792549e'
    url = 'https://api.covidactnow.org/v2/states.json?apiKey=' + covid_api
    data = requests.get(url)
    state_list = data.json()
    return state_list

@app.route("/us")
def us_page():
    state_list = api_handler()
    headings = ("State", "Cases", "Deaths", "Vaccinations Completed")
    output = []

    for state in state_list:
        metrics = (f"{state.get('state')}", f"{state.get('actuals').get('cases')}", f"{state.get('actuals').get('deaths')}",
        f"{state.get('actuals').get('vaccinationsCompleted')}")
        output.append(metrics)

    return render_template("country.html", headings=headings, output=output)

@app.route("/us/<state>-<abbrev>")
def state(state, abbrev):
    in_state = state
    in_abbrev = abbrev
    
    
    states = api_handler()
    abbrev = abbrev.upper()
    
    headings = ("State", "Cases", "Deaths", "Vaccinations")

    for state in states:
        if state.get('state') == abbrev:
            case_numbers = state.get('actuals').get('cases')
            deaths = state.get('actuals').get('deaths')
            vaccine = state.get('actuals').get('vaccinationsCompleted')
            break

    return render_template("state.html", in_state=in_state, in_abbrev=in_abbrev, case_numbers=case_numbers, headings=headings
    , deaths=deaths, vaccine=vaccine)

us_state_abbrev = {
    'alabama': 'al',
    'alaska': 'ak',
    'american samoa': 'as',
    'arizona': 'az',
    'arkansas': 'ar',
    'california': 'ca',
    'colorado': 'co',
    'connecticut': 'ct',
    'delaware': 'de',
    'district of columbia': 'dc',
    'florida': 'fl',
    'georgia': 'ga',
    'guam': 'gu',
    'hawaii': 'hi',
    'idaho': 'id',
    'illinois': 'il',
    'indiana': 'in',
    'iowa': 'ia',
    'kansas': 'ks',
    'kentucky': 'ky',
    'louisiana': 'la',
    'maine': 'me',
    'maryland': 'md',
    'massachusetts': 'ma',
    'michigan': 'mi',
    'minnesota': 'mn',
    'mississippi': 'ms',
    'missouri': 'mo',
    'montana': 'mt',
    'nebraska': 'ne',
    'nevada': 'nv',
    'new hampshire': 'nh',
    'new jersey': 'nj',
    'new mexico': 'nm',
    'new york': 'ny',
    'north carolina': 'nc',
    'north dakota': 'nd',
    'northern mariana islands':'mp',
    'ohio': 'oh',
    'oklahoma': 'ok',
    'oregon': 'or',
    'pennsylvania': 'pa',
    'puerto rico': 'pr',
    'rhode island': 'ri',
    'south carolina': 'sc',
    'south dakota': 'sd',
    'tennessee': 'tn',
    'texas': 'tx',
    'utah': 'ut',
    'vermont': 'vt',
    'virgin islands': 'vi',
    'virginia': 'va',
    'washington': 'wa',
    'west virginia': 'wv',
    'wisconsin': 'wi',
    'wyoming': 'wy'
}

# Example of templating
@app.route('/index')
def index():
    message = "Hello from my template! The time is: " + str(dt.now())
    image = url_for('static', filename='images/logo.png')
    return render_template('index.html', message=message, image=image)