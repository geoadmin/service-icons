import os

from flask import url_for

from app.helpers.description import find_descripton_file
from app.helpers.icons import get_icon_set_template_url
from app.helpers.url import get_base_url
from app.icon import Icon
from app.settings import COLORABLE_ICON_SETS
from app.settings import IMAGE_FOLDER
from app.settings import LEGACY_ICON_SETS


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


def get_all_icon_sets():
    icon_sets = []
    for root, dirs, files in os.walk(IMAGE_FOLDER):
        for icon_set_name in dirs:
            # icons of legacy icon sets are still available, but the icon set will not be listed
            if icon_set_name not in LEGACY_ICON_SETS:
                icon_sets.append(get_icon_set(icon_set_name))
    return icon_sets


class IconSet:
    """
    Helper class that contains all relevant information for a given icon set served by this service.
    """

    def __init__(self, name, colorable):
        """
        Args:
            name (str): The name of this icon set (will be used to determine its filepath)
            colorable (bool): If this icon sets consists of icons that can be (re-)colored
        """
        self.name = name
        self.colorable = colorable

    def is_valid(self):
        """
        Checks if a folder named as this icon set's name is present in the images/static folder

        Returns:
            True if a folder with this icon set's name is found
        """
        if not self.name:
            return False
        icon_set_folder_path = os.path.join(IMAGE_FOLDER, self.name)
        return os.path.exists(icon_set_folder_path) and os.path.isdir(icon_set_folder_path)

    def get_icon_set_url(self):
        """
        Generate and return the URL to access this icon set's metadata

        Returns:
            the URL by which this icon set's metadata can be accessed on this service
        """
        return url_for('icon_set_metadata', icon_set_name=self.name, _external=True)

    def get_icons_url(self):
        """
        Generate and return the URL that will list metadata of all available icons of this icon set.

        Returns:
            the URL to list all available icons in this icon set
        """
        return url_for('icons_from_icon_set', icon_set_name=self.name, _external=True)

    def get_icon(self, icon_name):
        """
        Generate and return the URL to access the metadata of one specific icon of this icon set

        Returns:
            the URL to read metadata of one icon of this icon set
        """
        return Icon(f"{icon_name}", self)

    def get_all_icons(self):
        """
        Generate a list of all icons belonging to this icon set.

        Returns:
            A list of all icons from this icon set, or None if this icon set is not found in the
                folder "static/images"
        """
        if not self.is_valid():
            return None
        icons = []
        for root, dirs, files in os.walk(os.path.join(IMAGE_FOLDER, self.name)):
            for icon_filename in sorted(files):
                name_without_extension = os.path.splitext(icon_filename)[0]
                icons.append(self.get_icon(name_without_extension))
        return icons

    def serialize(self):
        """
        As we want to add "icons_url" to the __dict__, we can't really use a json.dumps to generate
        our JSON output. This function is here to generate a correct __dict__ so that Flask can then
        jsonify all what we want.

        Returns:
            A __dict__ containing all relevant information relevant to be exposed by this endpoint
                regarding this icon set's metadata
        """
        return {
            "name": self.name,
            "colorable": self.colorable,
            "icons_url": self.get_icons_url(),
            "template_url": get_icon_set_template_url(get_base_url()),
            "has_description": bool(find_descripton_file(self.name))
        }
