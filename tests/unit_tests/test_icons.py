import json

from flask import url_for

from tests.unit_tests.base_test import ServiceIconsUnitTests


class IconsTests(ServiceIconsUnitTests):

    def test_colorized_icon_with_invalid_scale_value(self):
        response = self.request_colorized_icon(scale='0x')
        self.assertEqual(
            response.status_code, 400, "Should return a HTTP 400 when a invalid scale value"
        )
        self.assertCors(response)
        self.assertIn('Cache-Control', response.headers)
        self.assertIn('max-age=3600', response.headers['Cache-Control'])
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json,
            {
                "error": {
                    "code": 400, "message": "Invalid scale must be a positive number"
                },
                "success": False
            }
        )

    def test_colorized_icon_with_wrong_rgb_value(self):
        response = self.request_colorized_icon(red=2155)
        self.assertEqual(
            response.status_code, 400, "Should return a HTTP 400 when a RGB value is out of range"
        )
        self.assertCors(response)
        self.assertIn('Cache-Control', response.headers)
        self.assertIn('max-age=3600', response.headers['Cache-Control'])
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

    def test_colorized_icon_with_invalid_rgb_value(self):
        response = self.request_colorized_icon(red='invalid')
        self.assertEqual(
            response.status_code, 400, "Should return a HTTP 400 when a RGB value is out of range"
        )
        self.assertCors(response)
        self.assertIn('Cache-Control', response.headers)
        self.assertIn('max-age=3600', response.headers['Cache-Control'])
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
        response = self.request_colorized_icon(icon_name="non_existent_dummy_icon")
        self.assertEqual(
            response.status_code, 400, msg="Should return a HTTP 400 when file not found"
        )
        self.assertIn('max-age=3600', response.headers['Cache-Control'])
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json, {
                "error": {
                    "code": 400, "message": "Icon not found in icon set"
                }, "success": False
            }
        )

    def test_colorized_icon_http_header_origin_restriction(self):
        response = self.request_colorized_icon(origin="www.dummy.com")
        self.check_response_not_allowed(
            response, msg="Should return HTTP 403 when origin is not authorized"
        )
        response = self.request_colorized_icon(origin="")
        self.check_response_not_allowed(
            response, msg="Should return HTTP 403 when origin is not authorized"
        )

    def test_colorized_icon_no_http_post_method_allowed_on_endpoint(self):
        response = self.app.post(
            url_for(
                'colorized_icon',
                icon_set_name="default",
                icon_name="001-marker",
                scale='1x',
                red=255,
                green=0,
                blue=0
            ),
            data=json.dumps({"url": "https://test.bgdi.ch/test"}),
            content_type="application/json",
            headers=self.default_header
        )
        self.assertEqual(
            response.status_code,
            405,
            msg="Should return HTTP 405 (method not allowed) when a request is made"
            " with HTTP POST"
        )
        self.assertCors(response)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json,
            {
                "error": {
                    "code": 405, "message": "The method is not allowed for the requested URL."
                },
                "success": False
            }
        )

    def test_icons_from_icon_set(self):
        response = self.app.get(
            url_for('icons_from_icon_set', icon_set_name="default"), headers=self.default_header
        )
        self.assertEqual(response.status_code, 200)
        self.assertCors(response)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIn('Cache-Control', response.headers)
        self.assertIn('max-age=', response.headers['Cache-Control'])
        self.assertTrue('success' in response.json)
        self.assertTrue(response.json['success'])
        self.assertTrue('items' in response.json)
        self.assertTrue(isinstance(response.json['items'], list))
        self.assertTrue(len(response.json['items']) > 0)
