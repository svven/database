# try:
from setuptools import setup, find_packages 
# except ImportError:
#     from distutils.core import setup

setup(
    name='svven-database',
    version='0.1',
    author='Alexandru Stanciu',
    author_email='ducu@svven.com',
    packages=find_packages(),
    url='https://bitbucket.org/svven/database',
    description='Database models and helpers working with SQLAlchemy.',
    install_requires=[
        'SQLAlchemy>=0.9.8',
        'alembic>=0.7.1',
        'hashids>=1.0.1',
    ],
)