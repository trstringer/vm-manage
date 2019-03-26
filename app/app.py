"""Management VM web app"""

from flask import Flask, jsonify

# pylint: disable=invalid-name
app = Flask(__name__)

@app.route('/')
def default_route():
    """Default root route"""

    return jsonify(dict(application='vm-manage'))
