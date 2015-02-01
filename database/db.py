"""
SQLAlchemy module for mapper configuration.
Similar to SQLAlchemy class from flask.ext.sqlalchemy.
"""
from . import config

from sqlalchemy import \
    create_engine, engine_from_config, func, event, \
    Column, ForeignKey, UniqueConstraint, CheckConstraint, \
    Boolean, DateTime, Enum, SmallInteger, Integer, BigInteger, String
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

prefix = 'sqlalchemy_'

## Engine
get_engine = lambda config: engine_from_config(
    { key: getattr(config, key) for key in config.__dict__ if key.startswith(prefix) }, 
    prefix=prefix)

## Session
def Session():
    engine = get_engine(config)
    get_session = sessionmaker(bind=engine, autoflush=False)
    return get_session()

session = scoped_session(Session)

def init_app(app):
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

## Model
Model = declarative_base()
Model.query = session.query_property()

## Create and drop all
def import_all():
    import auth, news, twitter

def create_all():
    import_all()
    Model.metadata.create_all(get_engine(config))

def drop_all():
    import_all()
    Model.metadata.drop_all(get_engine(config))
