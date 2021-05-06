import json
from unittest.mock import patch

from tests.unit_tests.base_test import ServiceIconsUnitTests
from tests.unit_tests.base_test import build_request_url_for_icon


class IconsTests(ServiceIconsUnitTests):

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
        self.check_response_not_allowed(response,
                                        msg="Should return HTTP 403 when origin is not authorized")
        response = self.request_colorized_icon(origin="")
        self.check_response_not_allowed(response,
                                        msg="Should return HTTP 403 when origin is not authorized")

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
