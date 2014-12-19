"""
Database utils.
"""
import time, calendar
from datetime import datetime

from urlparse import urlparse

from hashids import Hashids
h = Hashids(salt="5vv3n", min_length=5)


def munixtime(dt):
	"Convert datetime to unixtime."
	return calendar.timegm(dt.utctimetuple())

def mdatetime(ut):
	"Convert unixtime to datetime."
	return datetime.utcfromtimestamp(ut)

def urlsite(url):
    "Get site for URL."
    return urlparse(url).netloc

def slugify(id):
    "Get hashid for id."
    return h.encrypt(id)
    