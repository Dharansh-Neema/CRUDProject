from flask import Flask
from pymongo import MongoClient
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Set up MongoDB connection
client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['MONGO_DBNAME']]

@app.route("/")
def hello():
    return "Hello"

