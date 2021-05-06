import unittest

from app import app
from app.version import APP_VERSION


class CheckerTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        self.route_prefix = "/v4/icons"

    def tearDown(self):
        pass

    def test_checker(self):
        response = self.app.get(
            f"{self.route_prefix}/checker", headers={"Origin": "map.geo.admin.ch"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json, {"message": "OK", "success": True, "version": APP_VERSION})

    def test_checker_with_invalid_version(self):
        response = self.app.get("/v999/icons/checker", headers={"Origin": "map.geo.admin.ch"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json, {
                "error": {
                    "code": 400, "message": "unsupported version of service."
                },
                "success": False
            }
        )
