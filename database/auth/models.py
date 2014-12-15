"""
Auth models.
"""
from .. import db
# from flask.ext.login import UserMixin


class User(db.Model): #, UserMixin 
    "Authenticated user."

    __tablename__ = 'auth_users'

    id = db.Column(db.BigInteger, primary_key=True)

    screen_name = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String)
    profile_image_url = db.Column(db.String)

    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    reader = db.relationship('Reader', backref='auth_user', uselist=False)

    def __repr__(self):
        return '<Auth User (%s): %s>' % (self.id, self.screen_name)
