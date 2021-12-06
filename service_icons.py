'''Service launcher to use Flask without wsgi.py
'''
from app import app  # pylint: disable=unused-import
from app.helpers import init_logging

# Initialize Logging using JSON format for all loggers and using the Stream Handler.
init_logging()
