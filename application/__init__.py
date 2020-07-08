from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initializing the flask application configuration
app = Flask(__name__, instance_relative_config=False)

# Initializing database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def api_server():
    with app.app_context():
        # Imports
        from . import routes

        # Create tables for our models
        db.create_all()

        # Give back flask app to run.py
        return app
