import unittest

from app import app
from app.settings import ROUTE_PREFIX


def build_request_url_for_icon(icon_filename="marker-48@2x.png",
                               red=255,
                               green=0,
                               blue=0,
                               icon_category="default"):
    return f"{ROUTE_PREFIX}/{icon_category}/{red},{green},{blue}/{icon_filename}"


class ServiceIconsUnitTests(unittest.TestCase):

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
                               origin="map.geo.admin.ch"):
        return self.app.get(
            build_request_url_for_icon(icon_filename, red, green, blue, icon_category),
            headers={"Origin": origin}
        )

    def check_response_not_allowed(self, response, msg):
        self.assertEqual(response.status_code,
                         403,
                         msg=msg)
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
