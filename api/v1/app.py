#!/usr/bin/python3
""" REST API using Flask """
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ Handler for 404 errors """
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown(exception):
    """ Called after each request """
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
