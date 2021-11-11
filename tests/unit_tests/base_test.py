import re
import unittest

from app import app
from app.settings import ALLOWED_DOMAINS_PATTERN
from app.settings import ROUTE_PREFIX


def build_request_url_for_icon(
    icon_name="marker", scale='1x', red=255, green=0, blue=0, icon_category="default"
):
    return f"{ROUTE_PREFIX}/sets/{icon_category}" \
           f"/icons/{icon_name}@{scale}-{red},{green},{blue}.png"


ORIGIN_FOR_TESTING = "some_random_domain"


class ServiceIconsUnitTests(unittest.TestCase):

    def __init__(self, methodName: str):
        super().__init__(methodName=methodName)
        # check .env.test for Origin value
        self.origin_for_testing = ORIGIN_FOR_TESTING
        self.default_header = {"Origin": self.origin_for_testing}

    def setUp(self):
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
        icon_name="marker",
        scale='1x',
        red=255,
        green=0,
        blue=0,
        icon_category="default",
        # see .env.test
        origin=ORIGIN_FOR_TESTING
    ):
        return self.app.get(
            build_request_url_for_icon(icon_name, scale, red, green, blue, icon_category),
            headers={"Origin": origin}
        )

    def check_response_not_allowed(self, response, msg, is_checker=False):
        self.assertEqual(response.status_code, 403, msg=msg)
        self.assertCors(response, check_origin=False)
        if not is_checker:
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
