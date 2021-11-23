import logging
import re

from werkzeug.exceptions import HTTPException

from flask import Flask
from flask import abort
from flask import request
from flask.helpers import url_for

from app.helpers import make_error_msg
from app.helpers.service_icon_custom_serializer import CustomJSONEncoder
from app.settings import ALLOWED_DOMAINS_PATTERN
from app.settings import CACHE_CONTROL
from app.settings import CACHE_CONTROL_4XX

logger = logging.getLogger(__name__)
route_logger = logging.getLogger('app.routes')

# Standard Flask application initialisation

app = Flask(__name__)
app.config.from_object('app.settings')
app.json_encoder = CustomJSONEncoder


# NOTE it is better to have this method registered first (before validate_origin) otherwise
# the route might not be logged if another method reject the request.
@app.before_request
def log_route():
    route_logger.info('%s %s', request.method, request.path)


# Add CORS Headers to all request
@app.after_request
def add_cors_header(response):
    # Do not add CORS header to internal /checker endpoint.
    if request.endpoint == 'checker':
        return response

    if (
        'Origin' in request.headers and
        re.match(ALLOWED_DOMAINS_PATTERN, request.headers['Origin'])
    ):
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


@app.after_request
def add_cache_control_header(response):
    if request.method == 'GET' and request.endpoint != 'checker':
        if response.status_code >= 400:
            response.headers.set('Cache-Control', CACHE_CONTROL_4XX)
        else:
            response.headers.set('Cache-Control', CACHE_CONTROL)
    return response


# Reject request from non allowed origins
@app.before_request
def validate_origin():
    if 'Origin' not in request.headers:
        logger.error('Origin header is not set')
        abort(403, 'Not allowed')
    if not re.match(ALLOWED_DOMAINS_PATTERN, request.headers['Origin']):
        logger.error('Origin=%s is not allowed', request.headers['Origin'])
        abort(403, 'Not allowed')


# Register error handler to make sure that every error returns a json answer
@app.errorhandler(Exception)
def handle_exception(err):
    """Return JSON instead of HTML for HTTP errors."""
    if isinstance(err, HTTPException):
        logger.error(err)
        return make_error_msg(err.code, err.description)

    logger.exception('Unexpected exception: %s', err)
    return make_error_msg(500, "Internal server error, please consult logs")


from app import routes  # isort:skip pylint: disable=wrong-import-position,cyclic-import
