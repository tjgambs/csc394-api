from app import db
from app.models.csc394_courses import Csc394Courses
from app.models.days_offered import DaysOffered

from sqlalchemy import and_


class TermCourses(db.Model):

    __tablename__ = "term_courses"

    stream = db.Column(db.String, primary_key=True)
    course_id = db.Column(db.String, primary_key=True)


    @staticmethod
    def getAvailableCourses(stream):
        """This function takes a stream and the moment it is greater than
        1005, then we wrap back around to 0975.
        """
        stream = TermCourses.convert_stream(stream)
        q = (db.session.query(
            Csc394Courses.subject,
            Csc394Courses.course_nbr,
            Csc394Courses.score,
            Csc394Courses.prereqs,
            DaysOffered.day)
            .join(DaysOffered, (and_(
                DaysOffered.subject == Csc394Courses.subject,
                DaysOffered.catalog_nbr == Csc394Courses.course_nbr)))
            .filter(DaysOffered.stream == stream)
            .order_by(Csc394Courses.score.desc(), Csc394Courses.id.desc()))

        return [TermCoursesEntity(row) for row in q.all()]

    @staticmethod
    def convert_stream(stream):
        quarter_range = 35
        student_quarter = int(stream)
        if student_quarter <= 1005:
            quarter = student_quarter
        else:
            quarter = ((student_quarter % quarter_range) + 975)
        stream = '0' + str(quarter) if quarter < 1000 else str(quarter)
        return stream


class TermCoursesEntity(object):

    def __init__(self, row):
        self.getName = row.subject.lower() + " " + str(row.course_nbr)
        self.score = row.score
        self.prereqs = row.prereqs
        self.day = row.day
