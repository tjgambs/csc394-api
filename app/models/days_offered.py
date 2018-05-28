from app import db


class DaysOffered(db.Model):

    __tablename__ = "days_offered"

    day = db.Column(db.String)
    stream = db.Column(db.String, primary_key = True)
    subject = db.Column(db.String)
    catalog_nbr = db.Column(db.Integer)
    section = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.String, primary_key = True)