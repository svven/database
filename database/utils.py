"""
Database utils.
"""
from urlparse import urlparse

from hashids import Hashids
h = Hashids(salt="5vv3n", min_length=5)


def urlsite(url):
    "Get site for URL."
    return urlparse(url).netloc

def slugify(id):
    "Get hashid for id."
    return h.encrypt(id)
    