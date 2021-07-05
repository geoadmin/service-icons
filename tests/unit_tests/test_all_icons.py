import io
import logging
import os

from PIL import Image

from app.helpers.icons import get_icon_template_url
from app.icon_set import get_icon_set
from app.settings import COLORABLE_ICON_SETS
from app.settings import IMAGE_FOLDER
from app.settings import ROUTE_PREFIX
from tests.unit_tests.base_test import ServiceIconsUnitTests


def get_average_color(pillow_image):
    """
    Return a tuple containing the average color of visible pixel in this image (checks only non
    transparent pixels, aka pixels with alpha greater than zero)
    Args:
        pillow_image: A pillow (PIL) Image
    """
    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    width, height = pillow_image.size
    # pylint: disable=invalid-name
    for x in range(0, width):
        for y in range(0, height):
            r, g, b, a = pillow_image.getpixel((x, y))
            # only checking non transparent pixels
            if a > 0:
                r_total += r
                g_total += g
                b_total += b
                count += 1
    # pylint: enable=invalid-name
    return r_total / count, g_total / count, b_total / count


class AllIconsTest(ServiceIconsUnitTests):
    """
    Tests using the folder static/images icons and thoroughly test them all
    """

    def setUp(self):
        super().setUp()
        # removing debug log of Pillow (otherwise it pollutes the unit test console output)
        logging.getLogger('PIL').setLevel(logging.INFO)
        # reading icons from static/images file and storing them as
        # dict{
        #    "icon_set_name_1": [ "icon_name1", "icon_name2", ... ],
        #    "icon_set_name_2": [...]
        # }
        self.all_icon_sets = {}
        for root, dirs, files in os.walk(os.path.join(IMAGE_FOLDER)):
            for icon_filename in files:
                icon_set_name = os.path.basename(root)
                icon_name = os.path.splitext(icon_filename)[0]
                if icon_set_name not in self.all_icon_sets:
                    self.all_icon_sets[icon_set_name] = []
                self.all_icon_sets[icon_set_name].append(icon_name)

    def check_image(
        self, icon_name, image_url, expected_size=48, check_color=False, red=255, green=0, blue=0
    ):
        """
        Retrieve an icon from the test instance and check everything related to this icon.
        It can also check that the average color corresponds to what is given in args.
        For that it will go through each (non-transparent) pixel, calculate the average color,
        and check that this average color correspond to any non-zero value given in args for RGB.
        (it doesn't check if it is a zero value, because some icons have edges that are not of
        the primary color, resulting in an average color that can't be "pure")
        """
        response = self.app.get(image_url, headers={"Origin": "map.geo.admin.ch"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/png")
        # reading the icon image so that we can check its size in px and average color
        with Image.open(io.BytesIO(response.data)) as icon:
            width, height = icon.size
            self.assertEqual(
                width,
                height,
                msg=f"Icons should be squares (wrong size of {width}px/{height}px"
                f" for icon : {icon_name})"
            )
            self.assertEqual(width, expected_size)
            if check_color:
                average_color = get_average_color(icon)
                error_message = f"Color mismatch for icon {icon_name}"
                acceptable_color_delta = 10
                if red > 0:
                    self.assertAlmostEqual(
                        red, average_color[0], delta=acceptable_color_delta, msg=error_message
                    )
                if green > 0:
                    self.assertAlmostEqual(
                        green, average_color[1], delta=acceptable_color_delta, msg=error_message
                    )
                if blue > 0:
                    self.assertAlmostEqual(
                        blue, average_color[2], delta=acceptable_color_delta, msg=error_message
                    )

    def test_all_icon_sets_endpoint(self):
        """
        Checking that the endpoint /sets returns all available icon sets
        """
        response = self.app.get(f"{ROUTE_PREFIX}/sets", headers={"Origin": "map.geo.admin.ch"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn('success', response.json)
        self.assertTrue(response.json['items'])
        self.assertIn('items', response.json)
        icon_sets_from_endpoint = response.json['items']
        self.assertEqual(len(icon_sets_from_endpoint), len(self.all_icon_sets))
        for icon_set in icon_sets_from_endpoint:
            self.assertIn('name', icon_set)
            self.assertTrue(icon_set['name'] in self.all_icon_sets)
            self.assertIn('colorable', icon_set)
            self.assertIn('icons_url', icon_set)

    def test_all_icon_sets_metadata_endpoint(self):
        """
        Checking that the endpoint /sets/{icon_set_name} returns all relevant information
        about an icon set, and that the icon URL given provides all available icons
        """
        for icon_set_name in self.all_icon_sets:
            with self.subTest(icon_set_name=icon_set_name):
                response = self.app.get(
                    f"{ROUTE_PREFIX}/sets/{icon_set_name}", headers={"Origin": "map.geo.admin.ch"}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content_type, "application/json")
                icon_set_metadata = response.json
                self.assertIn('name', icon_set_metadata)
                self.assertEqual(icon_set_name, icon_set_metadata['name'])
                self.assertIn('colorable', icon_set_metadata)
                self.assertIn('icons_url', icon_set_metadata)
                self.assertIsNotNone(icon_set_metadata['icons_url'])
                self.assertTrue(
                    icon_set_metadata['icons_url'].endswith(f"sets/{icon_set_name}/icons")
                )
                icons_response = self.app.get(
                    icon_set_metadata['icons_url'], headers={"Origin": "map.geo.admin.ch"}
                )
                self.assertEqual(icons_response.status_code, 200)
                self.assertEqual(icons_response.content_type, "application/json")
                self.assertIn('success', icons_response.json)
                self.assertTrue(icons_response.json['success'])
                self.assertIn('items', icons_response.json)
                self.assertEqual(
                    len(icons_response.json['items']), len(self.all_icon_sets[icon_set_name])
                )

    def test_all_icon_metadata_endpoint(self):
        """
        Checking all icons' URLs without giving the extension (should return icon's metadata)
        """
        for icon_set_name in self.all_icon_sets:
            for icon_name in self.all_icon_sets[icon_set_name]:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_metadata_url = f"{ROUTE_PREFIX}/sets/{icon_set_name}/icons/{icon_name}"
                    response = self.app.get(
                        icon_metadata_url, headers={"Origin": "map.geo.admin.ch"}
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.content_type, "application/json")
                    json_response = response.json
                    self.assertIn('icon_set', json_response)
                    self.assertEqual(icon_set_name, json_response['icon_set'])
                    self.assertIn('name', json_response)
                    self.assertEqual(icon_name, json_response['name'])
                    self.assertIn('template_url', json_response)
                    self.assertIsNotNone(json_response['template_url'])
                    self.assertTrue(json_response['template_url'].endswith(get_icon_template_url()))
                    self.assertIn('url', json_response)
                    self.assertIsNotNone(json_response['url'])
                    icon_url_without_color = f"{ROUTE_PREFIX}/sets/{icon_set_name}/icons"
                    if icon_set_name in COLORABLE_ICON_SETS:
                        self.assertTrue(
                            json_response['url'].
                            endswith(f"{icon_url_without_color}/{icon_name}@1x-255,0,0.png")
                        )
                    else:
                        self.assertTrue(
                            json_response['url'].
                            endswith(f"{icon_url_without_color}/{icon_name}@1x.png")
                        )

    def test_all_icon_basic_image(self):
        """
        Checking URLs without scale or color
        """
        for icon_set_name in self.all_icon_sets:
            for icon_name in self.all_icon_sets[icon_set_name]:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_url = f"{ROUTE_PREFIX}/sets/{icon_set_name}/icons/{icon_name}.png"
                    self.check_image(icon_name, icon_url)

    def test_all_icon_double_size(self):
        """
        Check URLs with "2x" as scale but no color
        """
        for icon_set_name in self.all_icon_sets:
            for icon_name in self.all_icon_sets[icon_set_name]:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    double_size_icon_url = f"{ROUTE_PREFIX}/sets/{icon_set_name}" \
                                           f"/icons/{icon_name}@2x.png"
                    self.check_image(icon_name, double_size_icon_url, expected_size=96)

    def test_all_icon_half_size(self):
        """
        Check URLs with "0.5x" as scale but no color
        """
        for icon_set_name in self.all_icon_sets:
            for icon_name in self.all_icon_sets[icon_set_name]:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    half_size_icon_url = f"{ROUTE_PREFIX}/sets/{icon_set_name}" \
                                         f"/icons/{icon_name}@0.5x.png"
                    self.check_image(icon_name, half_size_icon_url, expected_size=24)

    def test_all_icons_colorized(self):
        """
        Checks URLs with yellow color (no scaling)
        """
        for icon_set_name in self.all_icon_sets:
            for icon_name in self.all_icon_sets[icon_set_name]:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_set = get_icon_set(icon_set_name)
                    color_part = "-0,255,255" if icon_set.colorable else ""
                    colored_url = f"{ROUTE_PREFIX}/sets/{icon_set_name}" \
                                  f"/icons/{icon_name}{color_part}.png"
                    self.check_image(
                        icon_name,
                        colored_url,
                        check_color=icon_set.colorable,
                        red=0,
                        green=255,
                        blue=255
                    )

    def test_all_icons_colorized_and_double_size(self):
        """
        Checks URLs with blue color and double size
        """
        for icon_set_name in self.all_icon_sets:
            for icon_name in self.all_icon_sets[icon_set_name]:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_set = get_icon_set(icon_set_name)
                    color_part = "-0,0,255" if icon_set.colorable else ""
                    colored_url = f"{ROUTE_PREFIX}/sets/{icon_set_name}" \
                                  f"/icons/{icon_name}@2x{color_part}.png"
                    self.check_image(
                        icon_name,
                        colored_url,
                        check_color=icon_set.colorable,
                        expected_size=96,
                        red=0,
                        green=0,
                        blue=255
                    )

    def test_all_icons_colorized_and_half_size(self):
        """
        Checks URLs with green color and half size
        """
        for icon_set_name in self.all_icon_sets:
            for icon_name in self.all_icon_sets[icon_set_name]:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_set = get_icon_set(icon_set_name)
                    color_part = "-0,255,0" if icon_set.colorable else ""
                    colored_url = f"{ROUTE_PREFIX}/sets/{icon_set_name}/icons/" \
                                  f"{icon_name}@.5x{color_part}.png"
                    self.check_image(
                        icon_name,
                        colored_url,
                        check_color=icon_set.colorable,
                        expected_size=24,
                        red=0,
                        green=255,
                        blue=0
                    )
