import logging
import re

from werkzeug.exceptions import HTTPException

from flask import Flask
from flask import abort
from flask import request

from app.helpers import make_error_msg
from app.helpers.service_icon_custom_serializer import CustomJSONEncoder
from app.helpers.url import ALLOWED_DOMAINS_PATTERN
from app.middleware import ReverseProxy

logger = logging.getLogger(__name__)
route_logger = logging.getLogger('app.routes')

# Standard Flask application initialisation

app = Flask(__name__)
app.wsgi_app = ReverseProxy(app.wsgi_app, script_name='/')
app.json_encoder = CustomJSONEncoder


# NOTE it is better to have this method registered first (before validate_origin) otherwise
# the route might not be logged if another method reject the request.
@app.before_request
def log_route():
    route_logger.info('%s %s', request.method, request.path)


# Add CORS Headers to all request
@app.after_request
def add_cors_header(response):
    if (
        'Origin' in request.headers and
        re.match(ALLOWED_DOMAINS_PATTERN, request.headers['Origin'])
    ):
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response


# Reject request from non allowed origins
@app.before_request
def validate_origin():
    if 'Origin' in request.headers and \
        not re.match(ALLOWED_DOMAINS_PATTERN, request.headers['Origin']):
        logger.error('Origin=%s is not allowed', request.headers['Origin'])
        abort(make_error_msg(403, 'Not allowed'))


# Register error handler to make sure that every error returns a json answer
@app.errorhandler(HTTPException)
def handle_exception(err):
    """Return JSON instead of HTML for HTTP errors."""
    logger.error('Request failed code=%d description=%s', err.code, err.description)
    return make_error_msg(err.code, err.description)


from app import routes  # pylint: disable=wrong-import-position


def main():
    app.run()


if __name__ == '__main__':
    """
    Entrypoint for the application. At the moment, we do nothing specific, but there might be
    preparatory steps in the future
    """
    main()
