
from flask import abort, Blueprint, jsonify, request, abort, g
from app.utils import prepare_json_response
from app import app, db, auth, basicauth

from app.models.professors import Professors
from app.models.term_courses import TermCourses
from app.models.terms import Terms
from app.models.courses import Courses
from app.models.reviews import Reviews
from app.models.user import User
import requests


MOD = Blueprint("v1_admin", __name__, url_prefix="/v1/admin")


def is_admin(f):
    def is_admin(*args, **kwargs):
        if g.user.account_type != 2:
            abort(401)
        return f(*args, **kwargs)
    return is_admin


def is_not_student(f):
    def is_not_student(*args, **kwargs):
        if g.user.account_type == 0:
            abort(401)
        return f(*args, **kwargs)
    return is_not_student


@MOD.route("/get_students", methods=["GET"])
@auth.login_required
@is_not_student
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


@MOD.route("/delete_account/<id>", methods=["DELETE"])
@auth.login_required
@is_admin
def delete_account(id):
    acc = db.session.query(User).filter_by(id=id).first()
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
