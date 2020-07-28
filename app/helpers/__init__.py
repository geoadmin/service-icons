import os.path
from werkzeug.exceptions import BadRequest


def check_color_channels(r, g, b):
    """
    This function checks if a given color channel value is an integer and lies in the range of 0 to
    255. This function will be invoked from routes.py.
    If at least one parameter is ill defined, a BadRequest will be raised. Otherwise nothing
    will happen and there is no value returned.
    :param r: color channel value of the red channel.
    :param g: color channel value of the green channel.
    :param b: color channel value of the blue channel.
    :return: nothing.
    """
    if not (r.isdigit() and g.isdigit() and b.isdigit()):
        raise BadRequest('Color channel values must be integers.')
    elif not ((0 <= int(r) <= 255) and (0 <= int(g) <= 255) and (0 <= int(b) <= 255)):
        raise BadRequest('Color channel values must be integers in the range of 0 to 255.')


def check_path(path):
    """
    This function checks if the specified image file exists.
    This function will be invoked from routes.py.
    If everything is well defined, nothing special will happen here.
    Otherwise a BadRequest will be raised.
    :param image_name: path of the image file to be checked.
    :return: nothing.
    """
    if not os.path.isfile(path):
        raise BadRequest('The image to colorize doesn\'t exist')
