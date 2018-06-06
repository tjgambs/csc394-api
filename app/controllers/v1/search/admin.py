#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from app.utils import prepare_json_response
from app import db, auth
from app.controllers.v1.auth.auth import admin_access
from app.models.user import User


MOD = Blueprint("v1_admin", __name__, url_prefix="/v1/admin")


@MOD.route("/get_students", methods=["GET"])
@auth.login_required
@admin_access([1, 2])
def get_students():
    q = (db.session.query(User)
         .filter_by(account_type=0)
         .order_by(User.first_name, User.last_name))
    payload = [a.serialize for a in q.all()]

    data = {
        'columns': payload[0].keys() if payload else [],
        'rows': payload if payload else []
    }

    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=data
        )
    )


@MOD.route("/get_accounts", methods=["GET"])
@auth.login_required
@admin_access([2])
def get_accounts():
    q = (db.session.query(User)
         .filter(User.account_type != 2)
         .order_by(User.first_name, User.last_name))
    payload = [a.serialize for a in q.all()]

    data = {
        'columns': payload[0].keys() if payload else [],
        'rows': payload if payload else []
    }

    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=data
        )
    )


@MOD.route("/delete_account/<email>", methods=["DELETE"])
@auth.login_required
@admin_access([2])
def delete_account(email):
    db.session.query(User).filter_by(email=email).delete()
    return jsonify(
        prepare_json_response(
            message="OK",
            success=True
        )
    )
