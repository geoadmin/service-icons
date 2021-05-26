import os

from app.helpers.url import get_base_url
from app.icon import Icon
from app.settings import IMAGE_FOLDER


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
        return f"{get_base_url()}/{self.name}"

    def get_icons_url(self):
        """
        Generate and return the URL that will list metadata of all available icons of this icon set.

        Returns:
            the URL to list all available icons in this icon set
        """
        return f"{self.get_icon_set_url()}/icons"

    def get_icon(self, icon_name):
        """
        Generate and return the URL to access the metadata of one specific icon of this icon set

        Returns:
            the URL to read metadata of one icon of this icon set
        """
        return Icon(f"{icon_name}", self)

    def get_default_pixel_size(self):
        """
        Returns:
            the size in pixel of this icon set's icon (icons are always square images). This is
                helpful to calculate if an icon requires a resize before being served to the user.
        """
        if self.name == 'default':
            return 96
        return 48

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
            for icon_filename in files:
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
        return {"name": self.name, "colorable": self.colorable, "icons_url": self.get_icons_url()}
