"""
Auth models.
"""
import datetime

from .. import db


users_roles = db.Table('auth_users_roles',
    db.Model.metadata,
    db.Column('user_id', db.BigInteger, db.ForeignKey('auth_users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('auth_roles.id'))
)


class Role(db.Model):
    "User role."

    __tablename__ = 'auth_roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)

    def __repr__(self):
        return '<Auth Role: @%s>' % self.name


class User(db.Model):
    "Authenticated user."

    __tablename__ = 'auth_users'

    id = db.Column(db.BigInteger, primary_key=True)
    screen_name = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String)
    profile_image_url = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    
    active = db.Column(db.Boolean)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String)
    current_login_ip = db.Column(db.String)
    login_count = db.Column(db.Integer)

    reader = db.relationship('Reader', uselist=False)
    roles = db.relationship(Role, secondary=users_roles)

    def __init__(self, user):
        "Init with Twitter API `user`."
        self.load(user)

    def load(self, user):
        "Load user data from specified Twitter API `user`."
        self.screen_name = user.screen_name
        self.name = user.name
        self.profile_image_url = user.profile_image_url

    def __repr__(self):
        return '<Auth User (%s): %s>' % (self.id, self.screen_name)
