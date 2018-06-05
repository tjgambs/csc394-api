from app import db


class Wishlist(db.Model):

    __tablename__ = "wishlist"

    email = db.Column(db.String, primary_key=True)
    course = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, primary_key=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'course': self.course,
                'title': self.title}
