import json
from re import L

from flask import Flask, redirect, url_for, render_template, request, session, flash, make_response, \
    render_template_string
from decimal import Decimal
import pymongo
from flask_apscheduler import APScheduler
from os import environ
from dotenv import load_dotenv
from datetime import datetime as dt
from jinja2 import Environment
import dns, requests
from datetime import timedelta, datetime

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
        f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@cluster0-shard-00-00.kxem4.mongodb.net:27017,cluster0-shard-00-01.kxem4.mongodb.net:27017,cluster0-shard-00-02.kxem4.mongodb.net:27017/safetravels?ssl=true&replicaSet=atlas-5u7slz-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = db_client.safetravels
    return db


# Initial route to home
@app.route('/', methods=['GET', 'POST'])
def hello_flask():
    if request.method == 'POST':
        req = request.form
        state = req.get("state").lower()
        if state in us_state_abbrev:
            abbrev = us_state_abbrev.get(state)
            return redirect(f"/us/{state}-{abbrev}")
    return render_template('home.html')


# update API data into MongoDB
@scheduler.task('interval', id='update_mongo', hours=12, misfire_grace_time=1000)
@app.route('/mongo')
def update_mongo():
    db = connect_mongo()
    collection = db['new-state-list']
    state_list = api_handler()
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
    print(state_list)
    return state_list


@app.route("/compare", methods=["GET", "POST"])
def us_page():
    flag = 0
    if request.method == "POST":
        req = request.form
        state1 = req.get("state1").lower()
        state2 = req.get("state2").lower()
        if state1 in us_state_abbrev:
            flag = flag + 1
        if state2 in us_state_abbrev:
            if flag == 1:
                return redirect(f"/compare/{state1}-{state2}")
    return render_template("compare.html")

@app.route("/compare/<state1>-<state2>")
def compare2(state1, state2):
    db = connect_mongo()
    collection = db['new-state-list']

    headings = [state1, state2]

    abbrev1 = us_state_abbrev.get(state1).upper()
    abbrev2 = us_state_abbrev.get(state2).upper()


    vaccine_list1 = vaccineAdminMetrics(abbrev1)
    vaccine_list2 = vaccineAdminMetrics(abbrev2)
    dates1 = []
    dates2 = []
    infection_rate1 = []
    infection_rate2 = []
    vaccine_metrics1 = []
    vaccine_metrics2 = []

    for i in range(len(vaccine_list1)):
        dates1.append(vaccine_list1[i][0])
        vaccine_metrics1.append(vaccine_list1[i][1])
        infection_rate1.append(vaccine_list1[i][2])
    for i in range(len(vaccine_list2)):
        dates2.append(vaccine_list2[i][0])
        vaccine_metrics2.append(vaccine_list2[i][1])
        infection_rate2.append(vaccine_list2[i][2])
    for doc in list(collection.find()):
        if doc.get('state') == abbrev1:
            deaths1 = doc.get('actuals').get('deaths')
            break
    for doc in list(collection.find()):
        if doc.get('state') == abbrev2:
            deaths2 = doc.get('actuals').get('deaths')
            break

    print(deaths1)
    print(deaths2)

    return render_template("results.html",
        headings=headings,
        dates1=dates1,
        dates2=dates2,
        vaccine_metrics1=vaccine_metrics1,
        vaccine_metrics2=vaccine_metrics2,
        infection_rate1=infection_rate1,
        infection_rate2=infection_rate2,
        state1=state1,
        state2=state2,
        deaths1=deaths1,
        deaths2=deaths2,
        )

@app.route("/us/<state>-<abbrev>")
def state(state, abbrev):
    in_state = state
    in_abbrev = abbrev

    db = connect_mongo()
    collection = db['new-state-list']
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

    return render_template("state.html",
        in_state=in_state,
        in_abbrev=in_abbrev,
        case_numbers=case_numbers,
        headings=headings,
        deaths=deaths,
        vaccine=vaccine,
        dates=json.dumps(dates),
        vaccine_metrics=json.dumps(vaccine_metrics),
        infection_rate=json.dumps(infection_rate)
        )


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
    collection = db['new-state-list']

    vaccine_list = []

    for doc in list(collection.find()):
        if doc.get('state') == state_abb:
            metric = doc.get('metricsTimeseries')
            for i in range(len(metric)):
                if metric[i].get('date') >= "2020-14-12":
                    if metric[i].get('vaccinationsCompletedRatio'):
                        num = Decimal(metric[i].get('vaccinationsCompletedRatio'))
                        num = num * 100
                        line = (f"{metric[i].get('date')}", f"{str(num)}",
                        f"{metric[i].get('infectionRate')}")
                        vaccine_list.append(line)
            break
    return vaccine_list


@app.route('/flightAwareAPI')
def flightAwareAPI():
    return None

# App execution for dev branch
if __name__ == '__main__':
    app.run(debug=True)