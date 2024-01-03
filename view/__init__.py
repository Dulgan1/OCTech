#!/usr/bin/en python3
"""App View blueprint"""
from flask import Blueprint


app_view = Blueprint("app_view", __name__)

from view.blog import *
from view.post import *
