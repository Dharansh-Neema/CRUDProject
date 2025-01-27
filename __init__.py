# app/__init__.py

from flask import Flask
from pymongo import MongoClient
from config import Config
# from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Set up MongoDB connection
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client[app.config['MONGO_DBNAME']]

    # Import and register blueprints
    from . import routes
    app.register_blueprint(routes.user_bp, url_prefix='/users')

    @app.route('/')
    def index():
        return "Welcome to the User Profile CRUD API"

    return app
