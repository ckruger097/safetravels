from flask import Flask
from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv
import dns

app = Flask(__name__)

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
    return "Hello (from Flask)!"

# Example of using MongoDB
@app.route('/mongo')
def hello_mongo():
    db = connect_mongo()
    collection = db['safetravels-collection']
    result = collection.find({"string": {"$exists": True}})
    for doc in result:
        return str(doc.get("string"))


# App execution
if __name__ == '__main__':
    app.run(debug=True)
