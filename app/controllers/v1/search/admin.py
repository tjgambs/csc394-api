
from flask import abort, Blueprint, jsonify, request, abort, g
from app.utils import prepare_json_response
from app import app, db, auth, basicauth
from app.controllers.v1.auth.auth import admin_access



from app.models.professors import Professors
from app.models.term_courses import TermCourses
from app.models.terms import Terms
from app.models.courses import Courses
from app.models.reviews import Reviews
from app.models.user import User
import requests


MOD = Blueprint("v1_admin", __name__, url_prefix="/v1/admin")


@MOD.route("/get_students", methods=["GET"])
@auth.login_required
@admin_access([1,2])
def get_students():
    q = (db.session.query(User)
         .filter_by(account_type=0)
         .order_by(User.first_name, User.last_name))
    payload = [a.serialize for a in q.all()]

    data = {
        'columns': payload[0].keys(),
        'rows': payload
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
         .filter(User.account_type==0 | User.account_type==1)
         .order_by(User.first_name, User.last_name))
    payload = [a.serialize for a in q.all()]

    data = {
        'columns': payload[0].keys(),
        'rows': payload
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
    acc = db.session.query(User).filter_by(email=email).first()
    message = "FAILURE"
    if acc:
        acc.delete()
        db.session.commit()
        message = "OK"
    return jsonify(
        prepare_json_response(
            message=message,
            success=True
        )
    )
