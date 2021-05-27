import os

from app.settings import DEFAULT_COLOR
from app.settings import IMAGE_FOLDER


class Icon:
    """
    Helper class that contains all relevant information for a given icon served by this service.
    """

    def __init__(self, name, icon_set):
        """
        Args:
            name (str): The name of this icon (will be used to determine its filename)
            icon_set (IconSet): The icon set in which this icon belongs
        """
        self.name = name
        self.icon_set = icon_set

    def get_icon_url(
        self, red=DEFAULT_COLOR['r'], green=DEFAULT_COLOR['g'], blue=DEFAULT_COLOR['b']
    ):
        """
        Generate and returns the URL to access this icon's PNG image with this service.

        If color values are given, but the icon set is not colorable, colors will be ignored.

        Args:
            red: (int) red value (if this icon is part of an icon set that can be colorized)
            green: (int) green value (if this icon is part of an icon set that can be colorized)
            blue: (int) blue value (if this icon is part of an icon set that can be colorized)
        """
        color_part = ""
        if self.icon_set.colorable:
            color_part = f"-{red},{green},{blue}"
        return f"{self.icon_set.get_icon_set_url()}/icon/{self.name}{color_part}.png"

    def get_icon_filepath(self):
        """
        Returns an absolute path to the icon specified by its category and its name.
        It is advised to test if this path is valid after it is returned, there is no such
        check made in this function.

        Returns:
            A path leading to the file for this icon (can be an invalid one, do check its validity!)
        """
        name_with_extension = self.name
        if not name_with_extension.endswith('.png'):
            name_with_extension = f"{name_with_extension}.png"
        return os.path.abspath(os.path.join(IMAGE_FOLDER, self.icon_set.name, name_with_extension))

    def serialize(self):
        """
        As we want to add "url" to the __dict__, we can't really use a json.dumps to generate our
        JSON output. This function is here to generate a correct __dict__ so that Flask can then
        jsonify all what we want.

        Returns:
            A __dict__ containing all relevant information relevant to be exposed by this endpoint
                regarding this icon's metadata
        """
        return {
            "name": self.name,
            "icon_set": self.icon_set.name,
            "url": self.get_icon_url(),
        }
