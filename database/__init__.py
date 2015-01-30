"""
Database package defining all models.
"""
import config, db

## Models
from auth.models import *
from news.models import *
from twitter.models import *

def init(config_updates=None):
    """
    Delayed init to allow config updates.
    Updates can be passed as param here or set onto `config` upfront.
    i.e. `config.SETTING = updates.PREFIX_SETTING or updates.SETTING`
    """
    if config_updates:
        config.from_object(config_updates)
