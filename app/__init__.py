from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from app.utils import prepare_json_response
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
basicauth = HTTPBasicAuth()
auth = HTTPTokenAuth(scheme='Token')

from app.controllers import default
from app.controllers.v1.search import search
from app.controllers.v1.build import build
from app.controllers.v1.search import admin
from app.controllers.v1.user import user
from app.controllers.v1.auth import auth


app.register_blueprint(default.MOD)
app.register_blueprint(search.MOD)
app.register_blueprint(build.MOD)
app.register_blueprint(admin.MOD)
app.register_blueprint(auth.MOD)
app.register_blueprint(user.MOD)


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    if request.method == 'DELETE':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
app.after_request(add_cors_headers)



@app.errorhandler(400)
def forbidden400(error):
    """
    Renders 400 response
    :returns: JSON
    :rtype: flask.Response
    """
    return jsonify(
        prepare_json_response(
            message="Error 400: Bad request",
            success=False,
            data=error.description
        )
    ), 400

@app.errorhandler(401)
def forbidden401(error):
    """
    Renders 401 response
    :returns: JSON
    :rtype: flask.Response
    """
    return jsonify(
        prepare_json_response(
            message="Error 401: Unauthorized",
            success=False,
            data=error.description
        )
    ), 401
