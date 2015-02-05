Database
========

Database models and helpers working with SQLAlchemy.


Create (or drop) database
-------------------------

Using plain SQLAlchemy

```
$ . env/bin/activate
$ python
>>> from database import db
>>> db.create_all() # or db.drop_all()
```

Using Alembic migrations

```
$ . env/bin/activate
$ alembic init migrations
$ alembic revision --autogenerate -m "Initial revision"
$ alembic upgrade head
```

Running migrations
------------------

~ Perform any [detectable](http://alembic.readthedocs.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect) model changes and run

```
$ . env/bin/activate
$ alembic revision --autogenerate -m "Model change description"
$ alembic upgrade head
```
