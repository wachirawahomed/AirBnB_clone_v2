#!/usr/bin/python3
"""
Starts a Flask web application.
listen on 0.0.0.0, port 5000
routes: /: display "Hello HBNB!"
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Displays "Hello HBNB!" when accessing root URL.
    """
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
