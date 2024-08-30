import os

from flask import url_for

from app.helpers.description import get_icon_description
from app.helpers.icons import get_icon_template_url
from app.helpers.url import get_base_url
from app.settings import DEFAULT_COLOR
from app.settings import IMAGE_FOLDER

# Here we disable yapf to avoid putting spaces between fractional parts
# (`24/48` instead of `24 / 48`)
# yapf: disable

# Icon anchor is defined as [x, y] and as fractional. Here below we used the x and y in pixels
# to define the fraction with width=48px and height=48px
DEFAULT_ICON_ANCHOR = [24/48, 24/48]
ICON_ANCHORS = {
    '001-marker': [24/48, 42/48],
    '007-marker-stroked': [24/48, 42/48],
}
# yapf: enable


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
        self.anchor = ICON_ANCHORS.get(name, DEFAULT_ICON_ANCHOR)

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
        if self.icon_set.colorable:
            return url_for(
                'colorized_icon',
                icon_set_name=self.icon_set.name,
                icon_name=self.name,
                scale='1x',
                red=red,
                green=green,
                blue=blue,
                _external=True
            )
        return url_for(
            'colorized_icon',
            icon_set_name=self.icon_set.name,
            icon_name=self.name,
            scale='1x',
            _external=True
        )

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
            "anchor": self.anchor,
            "icon_set": self.icon_set.name,
            "url": self.get_icon_url(),
            "template_url": get_icon_template_url(get_base_url()),
            "description": get_icon_description(self.name, self.icon_set.name)
        }
