from flask import Blueprint
from flask_cors import CORS

api_view = Blueprint('api_view', __name__, url_prefix='/api/v1')
