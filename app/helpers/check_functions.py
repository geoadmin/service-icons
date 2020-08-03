from flask import abort
from app.helpers import make_error_msg


def check_color_channels(r, g, b):
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
    if not (r.isdigit() and g.isdigit() and b.isdigit()):
        abort(make_error_msg(400, "Color channel values must be integers."))
    elif not ((0 <= int(r) <= 255) and (0 <= int(g) <= 255) and (0 <= int(b) <= 255)):
        abort(
            make_error_msg(400, "Color channel values must be integers in the range of 0 to 255.")
        )
    return r, g, b
