import re
import unittest

from flask import url_for

from app import app
from app.settings import ALLOWED_DOMAINS_PATTERN

ORIGIN_FOR_TESTING = "some_random_domain"


class ServiceIconsUnitTests(unittest.TestCase):

    def __init__(self, methodName: str):
        super().__init__(methodName=methodName)
        # check .env.test for Origin value
        self.origin_for_testing = ORIGIN_FOR_TESTING
        self.default_header = {"Origin": self.origin_for_testing}

    def setUp(self):
        self.context = app.test_request_context()
        self.context.push()
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def assertCors(self, response, check_origin=True):  # pylint: disable=invalid-name
        if check_origin:
            self.assertIn('Access-Control-Allow-Origin', response.headers)
            self.assertTrue(
                re.match(ALLOWED_DOMAINS_PATTERN, response.headers['Access-Control-Allow-Origin'])
            )
        self.assertIn('Access-Control-Allow-Methods', response.headers)
        self.assertListEqual(
            sorted(['GET', 'HEAD', 'OPTIONS']),
            sorted(
                map(
                    lambda m: m.strip(),
                    response.headers['Access-Control-Allow-Methods'].split(',')
                )
            )
        )
        self.assertIn('Access-Control-Allow-Headers', response.headers)
        self.assertEqual(response.headers['Access-Control-Allow-Headers'], '*')

    def request_colorized_icon(
        self,
        icon_name="001-marker",
        scale='1x',
        red='255',
        green='0',
        blue='0',
        icon_category="default",
        # see .env.test
        origin=ORIGIN_FOR_TESTING
    ):
        return self.app.get(
            url_for(
                'colorized_icon',
                icon_set_name=icon_category,
                icon_name=icon_name,
                scale=scale,
                red=red,
                green=green,
                blue=blue
            ),
            headers={"Origin": origin}
        )

    def check_response_not_allowed(self, response, msg, is_checker=False):
        self.assertEqual(response.status_code, 403, msg=msg)
        if not is_checker:
            self.assertCors(response, check_origin=False)
            self.assertIn('Cache-Control', response.headers)
            self.assertIn('max-age=3600', response.headers['Cache-Control'])
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json, {
                "error": {
                    "code": 403, "message": "Not allowed"
                }, "success": False
            }
        )
