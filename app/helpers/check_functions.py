from flask import abort
from flask import current_app as capp
from app.helpers import make_error_msg

MAX_ALLOWED_VERSION = 4


def check_color_channels(r, g, b):  # pylint: disable=invalid-name
    """
    This function checks if a given color channel value is an integer and lies in the range of 0 to
    255. This function will be invoked from routes.py.
    If at least one parameter is ill defined, a BadRequest will be raised. Otherwise nothing
    will happen and there is no value returned.
    :param r: color channel value of the red channel.
    :param g: color channel value of the green channel.
    :param b: color channel value of the blue channel.
    :return:  verified r, g and b values.
    """
    if not ((0 <= r <= 255) and (0 <= g <= 255) and (0 <= b <= 255)):
        capp.logger.error("Color channel values must be integers in the range of 0 to 255.")
        abort(
            make_error_msg(400, "Color channel values must be integers in the range of 0 to 255.")
        )
    return r, g, b


def check_version(ver):
    """
    This function checks if the version number as defined in the route is  <= the maximum
    allowed version number. If not an error is raised.
    :param vers: version number as defined in the route.
    """
    if ver > MAX_ALLOWED_VERSION:
        abort(make_error_msg(400, "unsupported version of service."))
