"""
SQLAlchemy module for mapper configuration.
Similar to SQLAlchemy class from flask.ext.sqlalchemy.
"""
from . import config

from sqlalchemy import \
	create_engine, engine_from_config, func, event, \
    Column, ForeignKey, UniqueConstraint, CheckConstraint, \
    Boolean, DateTime, Enum, SmallInteger, Integer, BigInteger, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()

prefix = 'sqlalchemy_'

get_engine = lambda config: engine_from_config(
    { key: getattr(config, key) for key in config.__dict__ if key.startswith(prefix) }, 
    prefix=prefix)
get_session = sessionmaker()

def Session():
    engine = get_engine(config)
    get_session.configure(bind=engine)
    return get_session()

# Session = lambda: sessionmaker(bind=get_engine(config))()
# session = None # Session()

create_all = lambda: Model.metadata.create_all(get_engine(config))
drop_all = lambda: Model.metadata.drop_all(get_engine(config))
