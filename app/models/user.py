from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from app import app, db, cache
from app.models.curriculums import *
import datetime


class User(db.Model):

    __tablename__ = 'user'

    email = db.Column(db.String(), index=True, primary_key=True)
    password_hash = db.Column(db.String())
    token = db.Column(db.String(), index=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    account_type = db.Column(db.Integer())
    undergraduate_degree = db.Column(db.String())
    graduate_degree = db.Column(db.String())
    automation = db.Column(db.String())
    graduate_degree_concentration = db.Column(db.String())
    elective = db.Column(db.String())
    number_credit_hours = db.Column(db.String())
    starting_quarter = db.Column(db.String())

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=app.config['TOKEN_MAX_AGE'],):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        self.token = s.dumps({'email': self.email})
        db.session.commit()
        return self.token

    @property
    def account_type_string(self):
        if self.account_type == 0:
            return 'Student'
        if self.account_type == 1:
            return 'Faculty'
        if self.account_type == 2:
            return 'Admin'

    @property
    def serialize(self):
        return {'email': self.email,
                'token': self.token,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'account_type': self.account_type_string,
                'undergraduate_degree': self.undergraduate_degree,
                'graduate_degree': self.graduate_degree,
                'automation': self.automation,
                'graduate_degree_concentration': self.graduate_degree_concentration,
                'elective': self.elective,
                'number_credit_hours': self.number_credit_hours,
                'starting_quarter': self.starting_quarter}

    @property
    def curriculum(self):
        if self.graduate_degree == "Computer Science":
            return CS
        elif self.graduate_degree == "Information Science":
            if self.graduate_degree_concentration == 'Business Analysis/Systems Analysis':
                return IS_BA_SA
            elif self.graduate_degree_concentration == 'Business Intelligence':
                return IS_BI
            elif self.graduate_degree_concentration == 'IT Enterprise Management':
                return IS_IT
            else:
                raise ValueError('%s is not a supported concentration' %
                                 self.graduate_degree_concentration)
        else:
            raise ValueError('%s is not a supported degree' %
                             self.graduate_degree)

    @property
    def max_courses(self):
        return int(self.number_credit_hours) / 4

    @property
    def getCurriculum(self):
        if self.graduate_degree == "Computer Science":
            return "CS"
        if self.graduate_degree == "Information Science":
            return "IS"

    @property
    def getCoursesTaken(self):
        return set()

    @property
    def getTerm(self):
        if self.starting_quarter == 'Autumn':
            return '1000'
        if self.starting_quarter == 'Winter':
            return '0980'
        if self.starting_quarter == 'Spring':
            return '0985'
        return '0990'

    @property
    def getDegree_concentration(self):
        return self.graduate_degree_concentration

    @property
    def getCSFocus(self):
        if self.graduate_degree_concentration == "Software and Systems Development":
            return 5
        if self.graduate_degree_concentration == "Theory":
            return 6
        if self.graduate_degree_concentration == "Data Science":
            return 7
        if self.graduate_degree_concentration == "Database Systems":
            return 8
        if self.graduate_degree_concentration == "Artificial Intelligence":
            return 9
        if self.graduate_degree_concentration == "Software Engineering":
            return 10
        if self.graduate_degree_concentration == "Game and Real-Time Systems":
            return 11
        if self.graduate_degree_concentration == "Human-Computer Interaction":
            return 12

    @staticmethod
    @cache.memoize(app.config["CACHE_TIMEOUT"])
    def data_by_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return data

    @staticmethod
    def verify_auth_token(token):
        user_data = User.data_by_token(token)
        if user_data is None:
            return None
        user = db.session.query(User).filter(
            User.email == user_data['email']).first()
        if not user or user.token != token:
            return None
        return user
