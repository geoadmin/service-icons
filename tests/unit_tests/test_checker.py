from app.settings import ROUTE_PREFIX
from app.version import APP_VERSION
from tests.unit_tests.base_test import ServiceIconsUnitTests


class CheckerTests(ServiceIconsUnitTests):

    def test_checker(self):
        response = self.app.get(f"{ROUTE_PREFIX}/checker", headers=self.default_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertNotIn('Cache-Control', response.headers)
        self.assertEqual(response.json, {"message": "OK", "success": True, "version": APP_VERSION})

    def test_checker_denied_without_origin(self):
        response = self.app.get(f"{ROUTE_PREFIX}/checker", headers={"Origin": ""})
        self.check_response_not_allowed(
            response, msg="Should return HTTP 403 when origin is not authorized", is_checker=True
        )
