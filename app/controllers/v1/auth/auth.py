#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
from flask import Blueprint, jsonify, request, abort, g
from app.utils import prepare_json_response
from app.models.user import User
from app import app, db, auth, basicauth


MOD = Blueprint("v1_auth", __name__, url_prefix="/v1/auth")


def admin_access(argument):
    """ wrapper """

    def decorator(func):
        """ decorator """

        @wraps(func)
        def func_wrapper(*args, **kwargs):
            """ Actual function """
            has_access = False
            account_type = g.user.account_type
            for i in argument:
                if account_type and i == account_type:
                    has_access = True
                    break
            if not has_access:
                abort(401)

            return func(*args, **kwargs)

        return func_wrapper

    return decorator

@MOD.route('/user', methods=['POST'])
def new_user():
    if request.method == 'OPTIONS':
        return None
    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    account_type = request.json.get('accountType')
    if (email is None or password is None
            or first_name is None or last_name is None
            or account_type is None):
        abort(400)
    if User.query.filter_by(email=email).first() is not None:
        abort(400, 'Email already in use.')
    user = User(email=email, first_name=first_name,
                last_name=last_name, account_type=account_type)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    user.generate_auth_token(app.config['TOKEN_MAX_AGE'])
    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=user.serialize
        )
    )


@MOD.route('/user', methods=['GET'])
@auth.login_required
def get_user():
    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=g.user.serialize
        )
    )


@MOD.route('/update_user', methods=['POST'])
@auth.login_required
def update_user():
    if request.method == 'OPTIONS':
        return None

    email = request.json.get('email')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    undergraduate_degree = request.json.get('undergraduate_degree')
    graduate_degree = request.json.get('graduate_degree')
    automation = request.json.get('automation')
    graduate_degree_concentration = request.json.get(
        'graduate_degree_concentration')
    elective = request.json.get('elective')
    number_credit_hours = request.json.get('number_credit_hours')
    starting_quarter = request.json.get('starting_quarter')
    disallow_online = request.json.get('disallow_online')

    not_null = [email, first_name, last_name]
    if any(n is None for n in not_null): 
        abort(400)

    g.user.email = email
    g.user.first_name = first_name
    g.user.last_name = last_name
    g.user.undergraduate_degree = undergraduate_degree
    g.user.graduate_degree = graduate_degree
    g.user.automation = automation
    g.user.graduate_degree_concentration = graduate_degree_concentration
    g.user.elective = elective
    g.user.number_credit_hours = number_credit_hours
    g.user.starting_quarter = starting_quarter
    g.user.disallow_online = disallow_online
    db.session.commit()

    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=g.user.serialize
        )
    )


@MOD.route("/user/token", methods=["GET"])
@basicauth.login_required
def token():
    if request.method == 'OPTIONS':
        return None
    token = g.user.generate_auth_token(app.config['TOKEN_MAX_AGE'])
    return jsonify(
        prepare_json_response(
            message=None,
            success=True,
            data=g.user.serialize
        )
    )


@MOD.route("/user/verify", methods=["GET"])
@auth.login_required
def verify():
    return jsonify(
        prepare_json_response(
            message=None,
            success=True
        )
    )


@basicauth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        abort(401, 'The email you have entered is invalid.')
    if not user.verify_password(password):
        abort(401, 'The password you have entered is invalid.')
    g.user = user
    return True


@auth.verify_token
def verify_token(token):
    g.user = User.verify_auth_token(token)
    if not g.user:
        abort(401, 'Invalid User')
    elif g.user.token != token:
        abort(423, 'Your account has been automatically logged out due to activity on another device.')
    return True
