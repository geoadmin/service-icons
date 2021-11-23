from flask import request

from app.settings import SCRIPT_NAME


def get_base_url():
    """
    Generate the base URL for this service (the root endpoint at which this service is currently
    served). Useful if you want to generate URLs that points to any possible endpoint of this
    service without having to decipher where the service is hosted etc...

    Returns:
        The base endpoint for this service, where it is currently being served (or accessed)
    """
    # we need to remove either the trailing slash of request.host_url
    # or the prefix slash of SCRIPT_NAME (otherwise there are two slashes in between)
    base_url = f"{request.host_url[:-1]}{SCRIPT_NAME}"
    # if base_url ends with a /, this needs to be removed, as following parts of the route will
    # also begin with a / when added. Otherwise there would be // in the route.
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    return base_url
