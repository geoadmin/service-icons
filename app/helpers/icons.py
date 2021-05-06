import os
from flask import request

from app.settings import IMAGE_FOLDER
from app.settings import ROUTE_PREFIX


def get_all_icons(red=255, green=0, blue=0):
    """
    List all available icons and return them as dictionary entries with the following structure::

        {
            "category": "default|any folder found in static/images",
            "icon": "file name of the icon (with .png extension)",
            "url": "full URL to access this icon",
        }

    It will use red as the default color if none is defined as argument

    Args:
        red: red value for all icons' URL, between 0 and 255 (default: 255)
        green: green value for all icons' URL, between 0 and 255 (default: 0)
        blue: blue value for all icons' URL, between 0 and 255 (default: 0)
    Returns:
        A list of all available icons, described as dictionary entries (can be then later easily
            converted to JSON)
    """
    icon_sets = []
    for root, dirs, files in os.walk(IMAGE_FOLDER):
        for name in files:
            category = root.split(os.path.sep)[-1]
            icon_sets.append({
                "category": category,
                "icon": name,
                # we need to remove either the trailing slash of request.host_url
                # or the prefix slash of ROUTE_PREFIX (otherwise there are two slashes in between)
                "url":
                    f"{request.host_url}{ROUTE_PREFIX[1:]}/{category}/{red},{green},{blue}/{name}"
            })
    return icon_sets


def get_icon_filepath(icon_category, icon_name):
    """
    Returns an absolute path to the icon specified by its category and its name.
    It is advised to test if this path is valid after it is returned, there is no such
    check made in this function.

    Args:
        icon_category: the icon category (default or any other folder found in static/images/...)
        icon_name: the icon filename with its extension (.png)
    Returns:
        A path leading to the file for this icon (can be an invalid one, do check its validity!)
    """
    return os.path.abspath(os.path.join(IMAGE_FOLDER,
                                        icon_category,
                                        icon_name))
