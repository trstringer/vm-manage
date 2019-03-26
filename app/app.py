"""Management VM web app"""

from flask import Flask, jsonify

APP = Flask(__name__)

@APP.route('/')
def default_route():
    """Default root route"""

    return jsonify(dict(application='vm-manage'))
