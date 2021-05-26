import os

from app.icon_set import IconSet
from app.settings import COLORABLE_ICON_SETS
from app.settings import IMAGE_FOLDER


def get_all_icon_sets():
    icon_sets = []
    for root, dirs, files in os.walk(IMAGE_FOLDER):
        for icon_set_name in dirs:
            icon_sets.append(get_icon_set(icon_set_name))
    return icon_sets


def get_icon_set(icon_set_name):
    """
    Args:
        icon_set_name (str): The name of the icon set we want
    Returns:
        (IconSet): the icon set if found, or None if no icon set with this name is found
    """
    if icon_set_name:
        icon_set = IconSet(icon_set_name, icon_set_name in COLORABLE_ICON_SETS)
        # checking that this icon set really exists in the static/images folder
        if icon_set.is_valid():
            return icon_set
    return None
