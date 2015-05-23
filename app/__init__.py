# -*- coding: utf-8 -*-
__author__ = 'guti'


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

app = Flask(__name__)
app.config.from_object('config')
cache = Cache(app)
db = SQLAlchemy(app)

from app import views, models