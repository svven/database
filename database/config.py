"""
Config settings for the database.
"""
import os

def from_object(updates):
    "Update same name (or prefixed) settings."
    import sys
    config = sys.modules[__name__]
    
    prefix = config.__name__.split('.')[0].upper()
    keys = [k for k in config.__dict__ if \
        k != from_object.__name__ and not k.startswith('_')]
    get_value = lambda c, k: hasattr(c, k) and getattr(c, k) or None
    for key in keys:
        prefix_key = '%s_%s' % (prefix, key)
        value = get_value(updates, prefix_key) or get_value(updates, key)
        if value: setattr(config, key, value)

## SQLAlchemy
## http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
SQLALCHEMY_ECHO = sqlalchemy_echo = False
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
SQLALCHEMY_DATABASE_URI = sqlalchemy_url = 'postgresql://svven@%s/svven' % DATABASE_HOST
