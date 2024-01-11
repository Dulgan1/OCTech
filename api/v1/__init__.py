from flask import Blueprint
from flask_cors import CORS
from view import db_client

api_view = Blueprint('api_view', __name__, url_prefix='/api/v1')
CORS(api_view)
