#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, abort, g
from app.utils import prepare_json_response
from app import auth



MOD = Blueprint("v1_user", __name__, url_prefix="/v1/user")


@MOD.route('/add_to_wishlist/<id>', methods=['POST'])
@auth.login_required
def add_to_wishlist(id):
	pass