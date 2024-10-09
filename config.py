import os
from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api, Ressource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Bike, User, Login, SeralizerMixin

app = Flask(__name__)
CORS(app)


class Config:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['SQLALCHEMY-TRACK-MODIFICATIONS'] = False
    app.json.compact = False
    app.config[SECRET_KEY] = 'lazimakiumane'
    db = SQLAlchemy()
    db.init_app(app)
    Migrate = Migrate(app, db)
    bcrypt = Bcrypt(app)
    api = Api(app)
