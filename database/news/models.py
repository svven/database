"""
News models.
"""
from .. import db
from ..utils import slugify, urlsite, munixtime


class Link(db.Model):
    "News link data."

    __tablename__ = 'news_links'

    id = db.Column(db.BigInteger, primary_key=True)
    slug = db.Column(db.String, unique=True) #, nullable=False 
    url = db.Column(db.String, nullable=False, unique=True, index=True)
    site = db.Column(db.String)
    title = db.Column(db.String)
    image_url = db.Column(db.String)
    description = db.Column(db.String)
    broken = db.Column(db.Boolean)
    ignored = db.Column(db.Boolean) # e.g. http://apple.com

    picks = db.relationship('Pick', backref='link', lazy='dynamic')

    def __init__(self, summary):
        "Init with extracted `summary`."
        self.load(summary)

    def load(self, summary):
        "Load link data from specified extracted `summary`."
        self.url = summary.url
        self.site = urlsite(summary.url)
        self.title = summary.title
        self.image_url = summary.image and summary.image.url or None #.url
        self.description = summary.description

    def __repr__(self):
        return '<News Link (%s): %s>' % (self.slug, self.url)

@db.event.listens_for(Link, "after_insert")
def after_insert_link(mapper, connection, target):
    link_table = Link.__table__
    if target.slug is None:
        connection.execute(
            link_table.update().
            where(link_table.c.id==target.id).
            values(slug=slugify(target.id))
        )


class Reader(db.Model):
    "News reader accounts."

    __tablename__ = 'news_readers'

    id = db.Column(db.BigInteger, primary_key=True)
    auth_user_id = db.Column(db.BigInteger,
        db.ForeignKey('auth_users.id'), unique=True)
    twitter_user_id = db.Column(db.BigInteger,
        db.ForeignKey('twitter_users.user_id'), unique=True) #, nullable=False
    # facebook_user_id = db.Column(db.BigInteger,
    #     db.ForeignKey('facebook_users.user_id'), unique=True) #, nullable=False
    ignored = db.Column(db.Boolean)
    featured = db.Column(db.Integer)

    auth_user = db.relationship('database.auth.models.User', lazy='joined')
    twitter_user = db.relationship('database.twitter.models.User', lazy='joined')
    picks = db.relationship('Pick', backref='reader', lazy='dynamic')

    @property
    def is_user(self):
        return not self.auth_user_id is None

    @property
    def visible(self):
        return bool(self.is_user or self.featured)

    ## Proxy properties
    @property
    def screen_name(self):
        return (self.auth_user and self.auth_user.screen_name) or \
            (self.twitter_user and self.twitter_user.screen_name) or None

    @property
    def name(self):
        return (self.auth_user and self.auth_user.name) or \
            (self.twitter_user and self.twitter_user.name) or None

    @property
    def profile_image_url(self):
        return (self.auth_user and self.auth_user.profile_image_url) or \
            (self.twitter_user and self.twitter_user.profile_image_url) or None

    def __repr__(self):
        return '<News Reader (%s): @%s>' % (self.id, self.screen_name)


class Source:
    """
    Enum of pick sources.
    """
    values = (NONE, TWITTER, WEB, API) = ('none', 'twitter', 'web', 'api')


class Pick(db.Model):
    "News link picked by reader."

    __tablename__ = 'news_picks'
    __table_args__ = (
        # db.UniqueConstraint('link_id', 'reader_id'), # nope
    )

    id = db.Column(db.BigInteger, primary_key=True)
    link_id = db.Column(db.BigInteger, 
        db.ForeignKey('news_links.id'), nullable=False)
    reader_id = db.Column(db.BigInteger,
        db.ForeignKey('news_readers.id'), nullable=False)
    moment = db.Column(db.BigInteger, nullable=False) # created_at unix time
    source = db.Column(db.Enum(*Source.values, name='pick_sources'), nullable=False,
        default=Source.NONE) # TWITTER, WEB
    twitter_status_id = db.Column(db.BigInteger,
        db.ForeignKey('twitter_statuses.status_id'), unique=True) #, nullable=True
    # facebook_status_id = db.Column(db.BigInteger,
    #     db.ForeignKey('facebook_statuses.status_id'), unique=True) #, nullable=True
    # unpicked = db.Column(db.Boolean) #, nullable=False, default=False

    def __init__(self, status, reader_id):
        "Param `status` is a twitter.Status object."
        self.link_id = status.link_id
        self.reader_id = reader_id
        self.moment = munixtime(status.created_at)
        self.source = Source.TWITTER
        self.twitter_status_id = status.status_id

    def __repr__(self):
        return '<News Pick (%s): (%s, %s)>' % (self.id, self.link_id, self.reader_id)

