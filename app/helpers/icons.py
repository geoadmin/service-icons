import os

image_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static/images/'))


def get_all_icons(base_url, red=255, green=0, blue=0):
    """
    List all available icons and return them as dictionary entries with the following structure::

        {
            "category": "default|any folder found in static/images",
            "icon": "file name of the icon (with .png extension)",
            "url": "full URL to access this icon",
        }

    It will use red as the default color if none is defined as argument

    Args:
        base_url: Base URL of this server (e.g. http://localhost:5000 when doing a local serve, or
            any other DNS name this server has). This value can be extracted from the (flask)
            request itself by using `request.base_url`.
        red: red value for all icons' URL, between 0 and 255 (default: 255)
        green: green value for all icons' URL, between 0 and 255 (default: 0)
        blue: blue value for all icons' URL, between 0 and 255 (default: 0)
    Returns:
        A list of all available icons, described as dictionary entries (can be then later easily
            converted to JSON)
    """
    icon_sets = []
    for root, files in os.walk(image_folder):
        for name in files:
            category = root.split(os.path.sep)[-1]
            icon_sets.append({
                "category": category,
                "icon": name,
                "url": "{0}/{1}/{2},{3},{4}/{5}".format(base_url, category, red, green, blue, name)
            })
    return icon_sets
