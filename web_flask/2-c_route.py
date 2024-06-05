#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Displays "Hello HBNB!" when accessing root URL.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """
    Displays "HBNB" when accessing /hbnb URL.
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    """
    Displays "C " followed by the value of the text variable.
    Replace underscore _ symbols with a space.
    """
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
