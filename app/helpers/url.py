from flask import request

from app.settings import ALLOWED_DOMAINS
from app.settings import ROUTE_PREFIX

ALLOWED_DOMAINS_PATTERN = '({})'.format('|'.join(ALLOWED_DOMAINS))


def get_base_url():
    """
    Generate the base URL for this service (the root endpoint at which this service is currently
    served). Useful if you want to generate URLs that points to any possible endpoint of this
    service without having to decipher where the service is hosted etc...

    Returns:
        The base endpoint for this service, where it is currently being served (or accessed)
    """
    # we need to remove either the trailing slash of request.host_url
    # or the prefix slash of ROUTE_PREFIX (otherwise there are two slashes in between)
    return f"{request.host_url}{ROUTE_PREFIX[1:]}"
