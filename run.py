import json

from flask import Flask, redirect, url_for, render_template, request, session, flash, make_response, \
    render_template_string
import pymongo
from flask_apscheduler import APScheduler
from os import environ
from dotenv import load_dotenv
from datetime import datetime as dt
from jinja2 import Environment
import dns, requests, pycurl

app = Flask(__name__, template_folder='./app/templates', static_folder='./app/static')
app.config['SECRET_KEY'] = 'I figure if I study high, take the test high, get high scores! Right?'

# Scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

# .env necessary to connect to MongoDB
load_dotenv()
MONGO_USER = environ.get("MONGO_USER")
MONGO_PASSWORD = environ.get("MONGO_PASSWORD")


# Connect to Mongo. Will likely put in db folder or __init__.py
def connect_mongo():
    db_client = pymongo.MongoClient(
        f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.kxem4.mongodb.net/safetravels"
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


# update API data into MongoDB
@scheduler.task('interval', id='update_mongo', hours=12, misfire_grace_time=1000)
@app.route('/mongo')
def update_mongo():
    db = connect_mongo()
    collection = db['safetravels-collection']
    state_list = api_handler()
    for st in state_list:
        collection.update({"state": st.get('state')}, {"$set": st})
    
    return "Database updated with latest CoVID Act Now data"


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
    url = 'https://api.covidactnow.org/v2/states.timeseries.json?apiKey=' + covid_api
    data = requests.get(url)
    state_list = data.json()
    return state_list


@app.route("/us")
def us_page():
    headings = ("State", "Cases", "Deaths", "Vaccinations Completed")
    output = []

    db = connect_mongo()
    collection = db['safetravels-collection']
    
    for doc in list(collection.find()):
        metrics = (
            f"{doc.get('state')}", f"{doc.get('actuals').get('cases')}", f"{doc.get('actuals').get('deaths')}",
            f"{doc.get('actuals').get('vaccinationsCompleted')}")
        output.append(metrics)

    return render_template("country.html", headings=headings, output=output)


@app.route("/us/<state>-<abbrev>")
def state(state, abbrev):
    in_state = state
    in_abbrev = abbrev

    db = connect_mongo()
    collection = db['safetravels-collection']
    abbrev = abbrev.upper()

    headings = ("State", "Cases", "Deaths", "Vaccinations")

    vaccine_list = vaccineAdminMetrics(abbrev)
    dates = []
    vaccine_metrics = []
    infection_rate = []

    for i in range(len(vaccine_list)):
        dates.append(vaccine_list[i][0])
        vaccine_metrics.append(vaccine_list[i][1])
        infection_rate.append(vaccine_list[i][2])

    for doc in list(collection.find()):
        if doc.get('state') == abbrev:
            case_numbers = doc.get('actuals').get('cases')
            deaths = doc.get('actuals').get('deaths')
            vaccine = doc.get('actuals').get('vaccinationsCompleted')
            break

    return render_template("state.html", in_state=in_state, in_abbrev=in_abbrev, case_numbers=case_numbers,
                           headings=headings, deaths=deaths, vaccine=vaccine, dates=dates, vaccine_metrics=vaccine_metrics
                           , infection_rate=infection_rate)


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
    'northern mariana islands': 'mp',
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

def vaccineAdminMetrics(state_abb):
    db = connect_mongo()
    collection = db['safetravels-collection']
    
    vaccine_list = []

    for doc in list(collection.find()):
        if doc.get('state') == state_abb:
            metric = doc.get('metricsTimeseries')
            for i in range(len(metric)):
                if metric[i].get('date') >= "2020-14-12":
                    if metric[i].get('vaccinationsCompletedRatio'):
                        line = (f"{metric[i].get('date')}", f"{metric[i].get('vaccinationsCompletedRatio')}",
                        f"{metric[i].get('infectionRate')}")
                        vaccine_list.append(line)
            break
    return vaccine_list



# Example of templating
@app.route('/index')
def index():
    message = "Hello from my template! The time is: " + str(dt.now())
    image = url_for('static', filename='images/logo.png')
    return render_template('index.html', message=message, image=image)


@app.route('/flightAwareAPI')
def flightAwareAPI():
    return None