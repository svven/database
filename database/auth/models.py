"""
Auth models.
"""
import datetime

from .. import db


class User(db.Model):
    "Authenticated user."

    __tablename__ = 'auth_users'

    id = db.Column(db.BigInteger, primary_key=True)
    screen_name = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String)
    profile_image_url = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    registered_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    login_count = db.Column(db.Integer)
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String)

    reader = db.relationship('Reader', uselist=False)

    def __init__(self, **kwargs):
        "Base init or with Twitter API `user`."
        if 'user' in kwargs:
            self.load(kwargs['user'])
        else:
            super(User, self).__init__(**kwargs)

    def load(self, user):
        "Load user data from specified Twitter API `user`."
        self.screen_name = user.screen_name
        self.name = user.name
        self.profile_image_url = user.profile_image_url

    def __repr__(self):
        return '<Auth User (%s): %s>' % (self.id, self.screen_name)
