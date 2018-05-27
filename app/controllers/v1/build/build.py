
from flask import abort, Blueprint, jsonify, request, g
from app.utils import prepare_json_response
from app import app, db, auth, basicauth


from app.models.professors import Professors
from app.models.term_courses import TermCourses
from app.models.terms import Terms
from app.models.courses import Courses
from app.models.reviews import Reviews


MOD = Blueprint("v1_build", __name__, url_prefix="/v1/build")


@MOD.route("/auto_schedule", methods=["POST"])
@auth.login_required
def auto_schedule():

    data = g.user.serialize

    
    return jsonify(
        prepare_json_response(
            message="OK",
            success=True,
            data=data
        )
    )
