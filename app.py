#!/usr/bin/python3
"""OC Main App"""
from flask import Flask, render_template
from flask_ckeditor import CKEditor
from view import app_view, db_client
from os import getenv

app = Flask(__name__, template_folder='view/templates')
app.register_blueprint(app_view)
app.config['SECRET_KEY'] = getenv('OC_SECRET_KEY')
ckeditor = CKEditor(app)


@app.teardown_appcontext
def close_storage(error):
    """ Closes database storage connection on error"""
    db_client.close()


@app.errorhandler(404)
def error404(error):
    """ Error hanlder for 404 """
    return render_template('404.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
