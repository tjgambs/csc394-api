from app import db


class Csc394Courses(db.Model):

    __tablename__ = "csc394_courses"

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    subject = db.Column(db.String)
    course_nbr = db.Column(db.Integer)
    description = db.Column(db.String)
    prereqs = db.Column(db.String)
    score = db.Column(db.Integer)
    unlock_score = db.Column(db.Integer)
    rarity_score = db.Column(db.Integer)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'title': self.title,
                'subject': self.subject,
                'course_nbr': self.course_nbr,
                'description': self.description,
                'prereqs': self.prereqs,
                'score': self.score,
                'unlock_score': self.unlock_score,
                'rarity_score': self.rarity_score}
