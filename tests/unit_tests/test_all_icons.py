import io
import logging
import os

from nose2.tools import params
from PIL import Image

from flask import url_for

from app.helpers.icons import get_icon_template_url
from app.helpers.url import get_base_url
from app.icon_set import get_icon_set
from app.settings import COLORABLE_ICON_SETS
from app.settings import DEFAULT_ICON_SIZE
from app.settings import IMAGE_FOLDER
from app.settings import LEGACY_ICON_SETS
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
        self,
        icon_name,
        image_url,
        expected_size=DEFAULT_ICON_SIZE,
        check_color=False,
        red=255,
        green=0,
        blue=0
    ):
        """
        Retrieve an icon from the test instance and check everything related to this icon.
        It can also check that the average color corresponds to what is given in args.
        For that it will go through each (non-transparent) pixel, calculate the average color,
        and check that this average color correspond to any non-zero value given in args for RGB.
        (it doesn't check if it is a zero value, because some icons have edges that are not of
        the primary color, resulting in an average color that can't be "pure")
        """
        response = self.app.get(image_url, headers=self.default_header)
        self.assertEqual(response.status_code, 200)
        self.assertCors(response)
        self.assertEqual(response.content_type, "image/png")
        self.assertIn('Cache-Control', response.headers)
        self.assertIn('max-age=', response.headers['Cache-Control'])
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

    @params(
        {'Origin': 'map.geo.admin.ch'},
        {
            'Origin': 'map.geo.admin.ch', 'Sec-Fetch-Site': 'same-site'
        },
        {
            'Origin': 'public.geo.admin.ch', 'Sec-Fetch-Site': 'same-origin'
        },
        {
            'Origin': 'http://localhost', 'Sec-Fetch-Site': 'cross-site'
        },
        {'Sec-Fetch-Site': 'same-origin'},
        {'Referer': 'https://map.geo.admin.ch'},
    )
    def test_icon_set_origin_allowed(self, headers):
        response = self.app.get(url_for('all_icon_sets'), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertCors(response)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn('Cache-Control', response.headers, msg="Cache control header missing")
        self.assertIn(
            'max-age=', response.headers['Cache-Control'], msg="Cache Control max-age not set"
        )
        self.assertIn('success', response.json)
        self.assertIn('items', response.json)

    def test_all_icon_sets_endpoint(self):
        """
        Checking that the endpoint /sets returns all non-legacy icon sets
        """
        response = self.app.get(url_for('all_icon_sets'), headers=self.default_header)
        self.assertEqual(response.status_code, 200)
        self.assertCors(response)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn('Cache-Control', response.headers)
        self.assertIn('max-age=', response.headers['Cache-Control'])
        self.assertIn('success', response.json)
        self.assertIn('items', response.json)
        self.assertTrue(response.json['items'])
        icon_sets_from_endpoint = response.json['items']
        self.assertEqual(
            len(icon_sets_from_endpoint), len(self.all_icon_sets) - len(LEGACY_ICON_SETS)
        )
        for legacy_icon_set in LEGACY_ICON_SETS:
            self.assertNotIn(
                legacy_icon_set, icon_sets_from_endpoint, msg="Icon set should not be listed"
            )
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
        for icon_set_name, icon_set in self.all_icon_sets.items():
            with self.subTest(icon_set_name=icon_set_name):
                response = self.app.get(
                    url_for('icon_set_metadata', icon_set_name=icon_set_name),
                    headers=self.default_header
                )
                self.assertEqual(response.status_code, 200)
                self.assertCors(response)
                self.assertEqual(response.content_type, "application/json")
                self.assertIn('Cache-Control', response.headers)
                self.assertIn('max-age=', response.headers['Cache-Control'])
                icon_set_metadata = response.json
                self.assertIn('name', icon_set_metadata)
                self.assertEqual(icon_set_name, icon_set_metadata['name'])
                self.assertIn('colorable', icon_set_metadata)
                self.assertIn('has_description', icon_set_metadata)
                self.assertIn('icons_url', icon_set_metadata)
                self.assertIsNotNone(icon_set_metadata['icons_url'])
                self.assertEqual(
                    icon_set_metadata['icons_url'],
                    url_for('icons_from_icon_set', icon_set_name=icon_set_name, _external=True)
                )
                url = url_for('icons_from_icon_set', icon_set_name=icon_set_metadata["name"])
                icons_response = self.app.get(url, headers=self.default_header)
                self.assertEqual(icons_response.status_code, 200)
                self.assertEqual(icons_response.content_type, "application/json")
                self.assertIn('success', icons_response.json)
                self.assertTrue(icons_response.json['success'])
                self.assertIn('items', icons_response.json)
                self.assertEqual(len(icons_response.json['items']), len(icon_set))

    def test_all_icon_metadata_endpoint(self):
        """
        Checking all icons' URLs without giving the extension (should return icon's metadata)
        """
        for icon_set_name, icon_set in self.all_icon_sets.items():
            for icon_name in icon_set:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_metadata_url = url_for(
                        'icon_metadata', icon_set_name=icon_set_name, icon_name=icon_name
                    )
                    response = self.app.get(icon_metadata_url, headers=self.default_header)
                    self.assertEqual(response.status_code, 200)
                    self.assertCors(response)
                    self.assertEqual(response.content_type, "application/json")
                    self.assertIn('Cache-Control', response.headers)
                    self.assertIn('max-age=', response.headers['Cache-Control'])
                    json_response = response.json
                    self.assertIn('icon_set', json_response)
                    self.assertEqual(icon_set_name, json_response['icon_set'])
                    self.assertIn('description', json_response)
                    if json_response['description']:
                        self.assertIn('de', json_response['description'])
                        self.assertIn('fr', json_response['description'])
                        self.assertIn('it', json_response['description'])
                    self.assertIn('name', json_response)
                    self.assertEqual(icon_name, json_response['name'])
                    self.assertIn('template_url', json_response)
                    self.assertIsNotNone(json_response['template_url'])
                    self.assertEqual(
                        json_response['template_url'], get_icon_template_url(get_base_url())
                    )
                    self.assertIn('url', json_response)
                    self.assertIsNotNone(json_response['url'])
                    if icon_set_name in COLORABLE_ICON_SETS:
                        self.assertEqual(
                            json_response['url'],
                            url_for(
                                'colorized_icon',
                                icon_set_name=icon_set_name,
                                icon_name=icon_name,
                                red="255",
                                green="0",
                                blue="0",
                                scale='1x',
                                _external=True
                            )
                        )
                    else:
                        self.assertEqual(
                            json_response['url'],
                            url_for(
                                'colorized_icon',
                                icon_set_name=icon_set_name,
                                icon_name=icon_name,
                                scale='1x',
                                _external=True
                            )
                        )
                    self.assertIn('anchor', json_response)
                    self.assertIsInstance(
                        json_response['anchor'],
                        list,
                        msg='"anchor" should be a list with x and y fraction'
                    )
                    self.assertEqual(
                        len(json_response['anchor']),
                        2,
                        msg='"anchor" should have two items; x and y fraction'
                    )
                    for fraction in json_response['anchor']:
                        self.assertIsInstance(
                            fraction, (int, float), msg='"anchor" fraction should be int or float'
                        )
                        self.assertTrue(fraction > 0, msg='"anchor" fraction should be > 0')

                    self.assertIn('size', json_response)
                    self.assertIsInstance(
                        json_response['size'],
                        list,
                        msg='"size" should be a list with x and y dimension'
                    )
                    self.assertEqual(
                        len(json_response['size']), 2, msg='"size" should have two items; x and y'
                    )
                    for elem in json_response['size']:
                        self.assertIsInstance(elem, (int), msg='"size" should be int')
                        self.assertTrue(
                            elem == DEFAULT_ICON_SIZE, msg='"size" should be equal to 48'
                        )

    def test_all_icon_basic_image(self):
        """
        Checking URLs without scale or color
        """
        for icon_set_name, icon_set in self.all_icon_sets.items():
            for icon_name in icon_set:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_url = url_for(
                        'colorized_icon', icon_set_name=icon_set_name, icon_name=icon_name
                    )
                    self.check_image(icon_name, icon_url)

    def test_all_icon_double_size(self):
        """
        Check URLs with "2x" as scale but no color
        """
        for icon_set_name, icon_set in self.all_icon_sets.items():
            for icon_name in icon_set:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    double_size_icon_url = url_for(
                        'colorized_icon', icon_set_name=icon_set_name, icon_name=icon_name, scale=2
                    )
                    self.check_image(
                        icon_name, double_size_icon_url, expected_size=DEFAULT_ICON_SIZE * 2
                    )

    def test_all_icon_half_size(self):
        """
        Check URLs with "0.5x" as scale but no color
        """
        for icon_set_name, icon_set in self.all_icon_sets.items():
            for icon_name in icon_set:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    half_size_icon_url = url_for(
                        'colorized_icon',
                        icon_set_name=icon_set_name,
                        icon_name=icon_name,
                        scale='0.5x'
                    )
                    self.check_image(
                        icon_name, half_size_icon_url, expected_size=DEFAULT_ICON_SIZE * 0.5
                    )

    def test_all_icons_colorized(self):
        """
        Checks URLs with yellow color (no scaling)
        """
        for icon_set_name, icon_set in self.all_icon_sets.items():
            for icon_name in icon_set:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_set = get_icon_set(icon_set_name)
                    url_params = {"icon_set_name": icon_set_name, "icon_name": icon_name}
                    if icon_set.colorable:
                        url_params["red"] = 0
                        url_params["green"] = 255
                        url_params["blue"] = 255
                    colored_url = url_for('colorized_icon', **url_params)
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
        for icon_set_name, icon_set in self.all_icon_sets.items():
            for icon_name in icon_set:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_set = get_icon_set(icon_set_name)
                    url_params = {
                        "icon_set_name": icon_set_name, "icon_name": icon_name, "scale": '2x'
                    }
                    if icon_set.colorable:
                        url_params["red"] = 0
                        url_params["green"] = 0
                        url_params["blue"] = 255
                    colored_url = url_for('colorized_icon', **url_params)
                    self.check_image(
                        icon_name,
                        colored_url,
                        check_color=icon_set.colorable,
                        expected_size=DEFAULT_ICON_SIZE * 2,
                        red=0,
                        green=0,
                        blue=255
                    )

    def test_all_icons_colorized_and_half_size(self):
        """
        Checks URLs with green color and half size
        """
        for icon_set_name, icon_set in self.all_icon_sets.items():
            for icon_name in icon_set:
                with self.subTest(icon_set_name=icon_set_name, icon_name=icon_name):
                    icon_set = get_icon_set(icon_set_name)
                    url_params = {
                        "icon_set_name": icon_set_name, "icon_name": icon_name, "scale": '0.5x'
                    }
                    if icon_set.colorable:
                        url_params["red"] = 0
                        url_params["green"] = 255
                        url_params["blue"] = 0
                    colored_url = url_for('colorized_icon', **url_params)
                    self.check_image(
                        icon_name,
                        colored_url,
                        check_color=icon_set.colorable,
                        expected_size=DEFAULT_ICON_SIZE * 0.5,
                        red=0,
                        green=255,
                        blue=0
                    )
