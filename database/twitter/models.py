"""
Twitter models.
"""
import datetime

from .. import db


class User(db.Model):
    "Twitter user that is tweeting links."

    __tablename__ = 'twitter_users'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False, unique=True)
    screen_name = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    profile_image_url = db.Column(db.String)
    protected = db.Column(db.Boolean)
    friends_count = db.Column(db.Integer)
    followers_count = db.Column(db.Integer)
    ignored = db.Column(db.Boolean)

    token = db.relationship('Token', backref='user', uselist=False)
    timelines = db.relationship('Timeline', backref='user')
    statuses = db.relationship('Status', backref='user', lazy='dynamic')
    reader = db.relationship('Reader', uselist=False)

    def __init__(self, user, key=None, secret=None):
        "Init with Twitter API `user`."
        self.load(user)
        user_id = user.id
        self.user_id = user_id
        if key and secret:
            self.token = Token(user_id=user_id, key=key, secret=secret)
            self.timelines.append(Timeline(user_id=user_id))

    def load(self, user):
        "Load user data from specified Twitter API `user`."
        self.screen_name = user.screen_name
        self.name = user.name
        self.description = user.description
        self.profile_image_url = user.profile_image_url
        self.protected = user.protected
        self.friends_count = user.friends_count
        self.followers_count = user.followers_count

    def __repr__(self):
        return '<Twitter User (%s): @%s>' % (self.user_id, self.screen_name)


class Token(db.Model):
    "Twitter API access token for user."

    __tablename__ = 'twitter_tokens'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, 
        db.ForeignKey('twitter_users.user_id'), nullable=False, unique=True)
    key = db.Column(db.String, nullable=False)
    secret = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Twitter Token (%s): %s>' % (self.user_id, self.key.split('-')[1])


class State:
    """
    Enum of job states.
    Used for both the recurring TimelineJob and the StatusJob.
    """
    values = (NONE, BUSY, FAIL, DONE) = ('none', 'busy', 'fail', 'done')


class Timeline(db.Model):
    "Twitter timeline that is being polled."

    __tablename__ = 'twitter_timelines'

    class Type:
        "Enum of timeline types."
        values = (HOME, USER, LIST) = ('home', 'user', 'list')    

    DEFAULT_FREQUENCY = 15 * 60 # 15 mins
    MIN_FREQUENCY = 1 * 60 # 1 min
    MAX_FREQUENCY = 24 * 3600 # 1 day
    MAX_FAILURES = 3 # to keep enabled

    id = db.Column(db.BigInteger, primary_key=True)
    type = db.Column(db.Enum(*Type.values, name='timeline_types'), nullable=False,
        default=Type.HOME)
    user_id = db.Column(db.BigInteger, 
        db.ForeignKey('twitter_users.user_id'), nullable=False) #, unique=True
    list_id = db.Column(db.BigInteger, unique=True)
    since_id = db.Column(db.BigInteger)
    state = db.Column(db.Enum(*State.values, name='job_states'), nullable=False,
        default=State.NONE)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    next_check = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    prev_check = db.Column(db.DateTime)
    frequency = db.Column(db.Integer, nullable=False, default=DEFAULT_FREQUENCY)
    failures = db.Column(db.SmallInteger, nullable=False, default=0)

    def __repr__(self):
        return '<Twitter %s Timeline (%s): @%s>' % (self.type.capitalize(), 
            self.list_id or self.user_id, self.user.screen_name)


class Status(db.Model):
    "Twitter status with link tweeted by user."

    __tablename__ = 'twitter_statuses'

    id = db.Column(db.BigInteger, primary_key=True)
    status_id = db.Column(db.BigInteger, nullable=False, unique=True)
    user_id = db.Column(db.BigInteger, 
        db.ForeignKey('twitter_users.user_id'), nullable=False)
    url = db.Column(db.String, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    state = db.Column(db.Enum(*State.values, name='job_states'), nullable=False,
        default=State.NONE)
    link_id = db.Column(db.BigInteger, 
        db.ForeignKey('news_links.id'))

    link = db.relationship('Link', backref='twitter_statuses')
    pick = db.relationship('Pick', backref='twitter_status', uselist=False)

    def __init__(self, status):
        "Param `status` is a Twitter API status."
        self.status_id = status.id
        self.user_id = status.user.id
        self.created_at = status.created_at

    def __repr__(self):
        return '<Twitter Status (%s): %s>' % (self.status_id, self.url)

