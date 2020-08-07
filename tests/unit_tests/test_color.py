import unittest
import json

from app import app


class ColorTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        self.route_prefix = "/v4/color"

    def tearDown(self):
        pass

    def test_checker(self):
        response = self.app.get(
            f"{self.route_prefix}/checker", headers={"Origin": "map.geo.admin.ch"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json, {"message": "OK", "success": True})

        response = self.app.get("/v999/color/checker", headers={"Origin": "map.geo.admin.ch"})
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

    def test_color_errors(self):
        response = self.app.get(
            f"{self.route_prefix}/2155,0,0/marker-24@2x.png",
            headers={"Origin": "map.geo.admin.ch"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json,
            {
                "error":
                    {
                        "code": 400,
                        "message": "Color channel values must be integers in the range of 0 to 255."
                    },
                "success": False
            }
        )

        response = self.app.get(
            "/v999/color/255,0,0/marker-24@2x.png", headers={"Origin": "map.geo.admin.ch"}
        )
        self.assertEqual(response.status_code, 400, msg="unsupported service version.")
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json, {
                "error": {
                    "code": 400, "message": "unsupported version of service."
                },
                "success": False
            }
        )

        response = self.app.get(
            f"{self.route_prefix}/255,0,0/non_existent_dummy_file.png",
            headers={"Origin": "map.geo.admin.ch"}
        )
        self.assertEqual(response.status_code, 400, msg="File not found")
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.json,
            {
                "error": {
                    "code": 400, "message": "The image to colorize doesn't exist."
                },
                "success": False
            }
        )

    def test_color_domain_restriction(self):
        response = self.app.get(
            "/v4/color/255,0,0/marker-24@2x.png", headers={"Origin": "map.geo.admin.ch"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/png")

        response = self.app.post(
            f"{self.route_prefix}/255,0,0/marker-24@2x.png",
            data=json.dumps({"url": "https://test.bgdi.ch/test"}),
            content_type="application/json",
            headers={"Origin": "map.geo.admin.ch"}
        )
        self.assertEqual(response.status_code, 405, msg="POST method is not allowed")
        self.assertEqual(
            response.json,
            {
                "error":
                    {
                        "code": 405, "message": "The method is not allowed for the requested URL."
                    },
                "success": False
            }
        )

        response = self.app.get(
            "/v4/color/255,0,0/marker-24@2x.png", headers={"Origin": "www.dummy.com"}
        )
        self.assertEqual(response.status_code, 403, msg="ORIGIN must be set")
        self.assertEqual(
            response.json, {
                "error": {
                    "code": 403, "message": "Not allowed"
                }, "success": False
            }
        )
