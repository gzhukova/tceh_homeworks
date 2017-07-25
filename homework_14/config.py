import os

DEBUG=True
SECRET_KEY="Enemy"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Database settings:
SQLALCHEMY_DATABASE_URI = 'sqlite:///task_14.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False