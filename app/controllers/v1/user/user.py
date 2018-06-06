#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, abort, g
from app.utils import prepare_json_response
from app.models.wishlist import Wishlist
from app import app, db, auth, basicauth


MOD = Blueprint("v1_user", __name__, url_prefix="/v1/user")


@MOD.route('/add_to_wishlist/<course>/<title>', methods=['GET'])
@auth.login_required
def add_to_wishlist(course, title):
    try:
        item = Wishlist(email=g.user.email, course=course, title=title)
        db.session.add(item)
        db.session.commit()
        return jsonify(
            prepare_json_response(
                message="OK",
                success=True
            )
        )
    except:
        db.session.rollback()
        return jsonify(
            prepare_json_response(
                message="FAILURE",
                success=False
            )
        )


@MOD.route('/delete_from_wishlist/<course>/<title>', methods=['DELETE'])
@auth.login_required
def delete_from_wishlist(course, title):
    try:
        item = db.session.query(Wishlist).filter_by(
            email=g.user.email, course=course, title=title)
        if item:
            item.delete()
            db.session.commit()
        return jsonify(
            prepare_json_response(
                message="OK",
                success=True
            )
        )
    except:
        db.session.rollback()
        return jsonify(
            prepare_json_response(
                message="FAILURE",
                success=False
            )
        )


@MOD.route('/get_wishlist', methods=['GET'])
@auth.login_required
def get_wishlist():
    q = (db.session.query(Wishlist)
         .filter_by(email=g.user.email)
         .order_by(Wishlist.course))
    payload = [a.serialize for a in q.all()]
    data = {'results': payload}
    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=data
        )
    )
