#!/usr/bin/en python3
"""App View blueprint"""
from flask import Blueprint
from pymongo import MongoClient
from os import getenv

db_client = MongoClient(host=getenv('DB_HOST'), port=int(getenv('DB_PORT')))
app_view = Blueprint("app_view", __name__)

from view.blog import *
from view.post import *
