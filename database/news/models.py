"""
News models.
"""
from .. import db
from ..utils import slugify, urlsite


class Link(db.Model):
    "News link data."

    __tablename__ = 'news_links'

    id = db.Column(db.BigInteger, primary_key=True)
    slug = db.Column(db.String, unique=True) #, nullable=False 

    url = db.Column(db.String, nullable=False, unique=True)
    site = db.Column(db.String)
    title = db.Column(db.String)
    image_url = db.Column(db.String)
    description = db.Column(db.String)

    broken = db.Column(db.Boolean)
    known = db.Column(db.Boolean) # e.g. http://apple.com

    marks = db.relationship('Mark', backref='link', lazy='dynamic')

    def __init__(self, summary):
        "Param `summary` after extraction."
        self.url = summary.url
        self.site = urlsite(summary.url)
        self.title = summary.title
        self.image_url = summary.image #.url
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
    # flipboard_user_id = db.Column(db.BigInteger,
    #     db.ForeignKey('flipboard_users.user_id'), unique=True) #, nullable=False

    marks = db.relationship('Mark', backref='reader', lazy='dynamic')

    def __repr__(self):
        return '<News Reader (%s): @%s>' % (self.id, self.twitter_user.screen_name)


class Source:
    """
    Enum of mark sources.
    """
    values = (NONE, TWITTER, WEB, API) = ('none', 'twitter', 'web', 'api')


class Mark(db.Model):
    "News link marked as interesting by reader."

    __tablename__ = 'news_marks'
    __table_args__ = (
        # db.UniqueConstraint('link_id', 'reader_id'), # nope
    )

    id = db.Column(db.BigInteger, primary_key=True)

    link_id = db.Column(db.BigInteger, 
        db.ForeignKey('news_links.id'), nullable=False)
    reader_id = db.Column(db.BigInteger,
        db.ForeignKey('news_readers.id'), nullable=False)
    moment = db.Column(db.BigInteger, nullable=False) # created_at unix time
    
    source = db.Column(db.Enum(*Source.values, name='mark_sources'), nullable=False,
        default=Source.NONE) # TWITTER, WEB

    unmarked = db.Column(db.Boolean) #, nullable=False, default=False

