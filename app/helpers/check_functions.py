import logging
import os

from flask import abort

from app.helpers import make_error_msg
from app.helpers.icons import get_icon_set

logger = logging.getLogger(__name__)


def __check_color(color):
    return 0 <= color <= 255


def check_color_channels(red, green, blue):
    """
    This function checks if a given color channel value is an integer and lies in the range of 0 to
    255. This function will be invoked from routes.py.
    If at least one parameter is ill defined, a BadRequest will be raised. Otherwise nothing
    will happen and there is no value returned.

    Args:
        red: (int) color channel value of the red channel.
        green: (int) color channel value of the green channel.
        blue: (int) color channel value of the blue channel.
    Return:
          verified r, g and b values.
    """
    if not (__check_color(red) and __check_color(green) and __check_color(blue)):
        logger.error(
            "Color channel values must be integers in the range of 0 to 255. "
            "(given: %d, %d, %d)",
            red,
            green,
            blue
        )
        abort(
            make_error_msg(400, "Color channel values must be integers in the range of 0 to 255.")
        )
    return red, green, blue


def get_and_check_icon_set(icon_set_name):
    """
    Checks that the icon set's name given in args corresponds to a valid icon set (that is found in
    '/static/images').
    Otherwise raises a Flask error and abort the current request.

    Args:
        icon_set_name: (str) the name of the wanted icon set (must correspond to a folder in
            'static/images')
    Returns:
        The icon set if found, otherwise raises a flask error and abort the current request
    """
    icon_set = get_icon_set(icon_set_name)
    if not icon_set:
        logger.error("Icon set not found: %s", icon_set_name)
        abort(make_error_msg(400, "Icon set not found"))
    return icon_set


def get_and_check_icon(icon_set, icon_name):
    """
    Checks that the icon with the name given in param exists in the icon set's folder.
    If so returns the metadata to this icon. Otherwise raises a flask error and abort the current
    request.

    Args:
        icon_set: (IconSet) the icon set in which belongs the icon we want
        icon_name: (str) the name of the icon
    """
    icon = icon_set.get_icon(icon_name)
    # checking that the icon exists in the icon set's folder
    path = icon.get_icon_filepath()
    if not os.path.isfile(path):
        logger.error("The icon doesn't exist: %s", path)
        abort(make_error_msg(400, "Icon not found in icon set"))
    return icon
