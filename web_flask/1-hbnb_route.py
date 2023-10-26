#!/usr/bin/python3
""" Hello Flask! """
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """ content of the home page """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_page():
    """ content of hbnb page """
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
