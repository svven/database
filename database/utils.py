"""
Database utils.
"""
from hashids import Hashids

h = Hashids(salt="5vv3n", min_length=5)


def slugify(id):
	"Get hashid for id."
	return h.encrypt(id)
	