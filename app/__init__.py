import logging
import re
import time

from werkzeug.exceptions import HTTPException

from flask import Flask
from flask import abort
from flask import g
from flask import request

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


def is_domain_allowed(domain):
    return re.match(ALLOWED_DOMAINS_PATTERN, domain) is not None


# NOTE it is better to have this method registered first (before validate_origin) otherwise
# the route might not be logged if another method reject the request.
@app.before_request
def log_route():
    g.setdefault('started', time.time())
    route_logger.debug('%s %s', request.method, request.path)


# Add CORS Headers to all request
@app.after_request
def add_cors_header(response):
    # Do not add CORS header to internal /checker endpoint.
    if request.endpoint == 'checker':
        return response

    response.headers['Access-Control-Allow-Origin'] = request.host_url
    if 'Origin' in request.headers and is_domain_allowed(request.headers['Origin']):
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    response.headers['Vary'] = 'Origin'
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
    # The Origin headers is automatically set by the browser and cannot be changed by the javascript
    # application. Unfortunately this header is only set if the request comes from another origin.
    # Sec-Fetch-Site header is set to `same-origin` by most of the browser except by Safari !
    # The best protection would be to use the Sec-Fetch-Site and Origin header, however this is
    # not supported by Safari. Therefore we added a fallback to the Referer header for Safari.
    sec_fetch_site = request.headers.get('Sec-Fetch-Site', None)
    origin = request.headers.get('Origin', None)
    referrer = request.headers.get('Referer', None)

    if origin is not None:
        if is_domain_allowed(origin):
            return
        logger.error('Origin=%s does not match %s', origin, ALLOWED_DOMAINS_PATTERN)
        abort(403, 'Permission denied')

    # BGDIINF_SB-3115: Apparently IOS 16 has a bug and set Sec-Fetch-Site=cross-site even if the
    # request is originated (same origin and/or referrer) from the same site ! Therefore to avoid
    # issue on IOS we first checks the referrer before checking Sec-Fetch-Site even if this not
    # correct.
    if referrer is not None:
        if is_domain_allowed(referrer):
            return
        logger.error('Referer=%s does not match %s', referrer, ALLOWED_DOMAINS_PATTERN)
        abort(403, 'Permission denied')

    if sec_fetch_site is not None:
        if sec_fetch_site in ['same-origin', 'same-site']:
            return
        logger.error('Sec-Fetch-Site=%s is not allowed', sec_fetch_site)
        abort(403, 'Permission denied')

    logger.error('Referer and/or Origin and/or Sec-Fetch-Site headers not set')
    abort(403, 'Permission denied')


@app.after_request
def log_response(response):
    logger.info(
        "%s %s - %s",
        request.method,
        request.path,
        response.status,
        extra={
            'response': {
                "status_code": response.status_code, "headers": dict(response.headers.items())
            },
            "duration": time.time() - g.get('started', time.time())
        }
    )
    return response


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
