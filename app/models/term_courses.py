from app import db
from app.models.csc394_courses import Csc394Courses
from app.models.days_offered import DaysOffered


class TermCourses(db.Model):

    __tablename__ = "term_courses"

    stream = db.Column(db.String, primary_key=True)
    course_id = db.Column(db.String, primary_key=True)


    @staticmethod
    def getOptions(stream):
        quarter_range = 45
        student_quarter = int(stream)
        if student_quarter <= 1005: # This was 1020
            quarter = student_quarter
        else:
            quarter = ((student_quarter % quarter_range) + 975)

        if quarter < 1000:
            stream = '0' + str(quarter)
        else:
            stream = str(quarter)

        #q = (db.session.query(Csc394Courses.subject, Csc394Courses.course_nbr, Csc394Courses.score, Csc394Courses.prereqs, DaysOffered.day)
        #     .join(DaysOffered, (DaysOffered.subject == Csc394Courses.subject and DaysOffered.catalog_nbr == Csc394Courses.course_nbr))
        #     .filter(DaysOffered.stream == stream )
        #     .order_by(Csc394Courses.score))

        q = (db.session.query(Csc394Courses.subject, Csc394Courses.course_nbr, Csc394Courses.score, Csc394Courses.prereqs, DaysOffered.day)
              .join(DaysOffered, (DaysOffered.subject == Csc394Courses.subject and DaysOffered.catalog_nbr == Csc394Courses.course_nbr))
              .filter(DaysOffered.stream == stream )
              .order_by(Csc394Courses.score.desc()))

        return [result(row) for row in q.all()]

class result(object):

    def __init__(self, row):
        self.getName = row.subject.lower() + " " + str(row.course_nbr)
        self.score = row.score
        self.prereqs = row.prereqs
        self.day = row.day