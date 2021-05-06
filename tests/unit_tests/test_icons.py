import json
import unittest
from unittest.mock import patch

from app import app


def build_request_url_for_icon(icon_filename="marker-48@2x.png",
                               red=255,
                               green=0,
                               blue=0,
                               icon_category="default",
                               version=4):
    return f"/v{version}/icons/{icon_category}/{red},{green},{blue}/{icon_filename}"


class IconsTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def request_colorized_icon(self,
                               icon_filename="marker-48@2x.png",
                               red=255,
                               green=0,
                               blue=0,
                               icon_category="default",
                               version=4,
                               origin="map.geo.admin.ch"):
        return self.app.get(
            build_request_url_for_icon(icon_filename, red, green, blue, icon_category, version),
            headers={"Origin": origin}
        )

    def test_colorized_icon_with_wrong_rgb_value(self):
        response = self.request_colorized_icon(red=2155)
        self.assertEqual(response.status_code,
                         400,
                         "Should return a HTTP 400 when a RGB value is out of range")
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json,
            {
                "error": {
                    "code": 400,
                    "message": "Color channel values must be integers in the range of 0 to 255."
                },
                "success": False
            }
        )

    def test_colorized_icon_with_wrong_version(self):
        response = self.request_colorized_icon(version=999)
        self.assertEqual(response.status_code,
                         400,
                         msg="Should return a HTTP 400 for an unsupported service version.")
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json, {
                "error": {
                    "code": 400,
                    "message": "unsupported version of service."
                },
                "success": False
            }
        )

    def test_colorized_icon_non_existent_icon_name(self):
        response = self.request_colorized_icon(icon_filename="non_existent_dummy_file.png")
        self.assertEqual(response.status_code,
                         400,
                         msg="Should return a HTTP 400 when file not found")
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json,
            {
                "error": {
                    "code": 400,
                    "message": "The image to colorize doesn't exist."
                },
                "success": False
            }
        )

    def test_colorized_icon_http_header_origin_restriction(self):
        response = self.request_colorized_icon(origin="www.dummy.com")
        self.assertEqual(response.status_code,
                         403,
                         msg="Should return HTTP 403 when origin is not authorized")
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json,
            {
                "error": {
                    "code": 403,
                    "message": "Not allowed"
                },
                "success": False
            }
        )
        response = self.request_colorized_icon(origin="")
        self.assertEqual(response.status_code,
                         403,
                         msg="Should return HTTP 403 when origin is not set")
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json,
            {
                "error": {
                    "code": 403,
                    "message": "Not allowed"
                },
                "success": False
            }
        )

    def test_colorized_icon_no_http_post_method_allowed_on_endpoint(self):
        request_url = build_request_url_for_icon()
        response = self.app.post(
            request_url,
            data=json.dumps({"url": "https://test.bgdi.ch/test"}),
            content_type="application/json",
            headers={"Origin": "map.geo.admin.ch"}
        )
        self.assertEqual(response.status_code,
                         405,
                         msg="Should return HTTP 405 (method not allowed) when a request is made"
                             " with HTTP POST")
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json,
            {
                "error": {
                    "code": 405,
                    "message": "The method is not allowed for the requested URL."
                },
                "success": False
            }
        )

    @patch('app.routes.get_all_icons')
    def test_all_icons(self, mock_get_all_icons):
        first_mock_icon = {
            "category": "default",
            "icon": "mocked_up_icon.png",
            "url": "http://fake_url_to_first_mock_icon"
        }
        second_mock_icon = {
            "category": "other",
            "icon": "another_mocked_up_icon.png",
            "url": "http://fake_url_to_second_mock_icon"
        }
        mock_get_all_icons.return_value = [first_mock_icon, second_mock_icon]

        response = self.app.get('/v4/icons/all', headers={"Origin": "map.geo.admin.ch"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertTrue(isinstance(response.json, list))
        self.assertEqual(len(response.json), 2)
        self.assertDictEqual(response.json[0], first_mock_icon)
        self.assertDictEqual(response.json[1], second_mock_icon)
