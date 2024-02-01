from flask import url_for

from app.version import APP_VERSION
from tests.unit_tests.base_test import ServiceIconsUnitTests


class CheckerTests(ServiceIconsUnitTests):

    def test_checker(self):
        response = self.app.get(url_for('checker'), headers=self.default_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertNotIn('Cache-Control', response.headers)
        self.assertEqual(response.json, {"message": "OK", "success": True, "version": APP_VERSION})
