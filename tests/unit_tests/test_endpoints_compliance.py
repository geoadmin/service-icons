from app.settings import ROUTE_PREFIX
from tests.unit_tests.base_test import ServiceIconsUnitTests


def remove_prefix_slash(value):
    if value.startswith('/'):
        return value[len('/'):]
    return value[:]


class CheckerTests(ServiceIconsUnitTests):

    def check_response_compliance(self, response, is_list_endpoint=False):
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue('success' in response.json)
        self.assertTrue(response.json['success'])
        if is_list_endpoint:
            self.assertTrue('items' in response.json)
            self.assertIsNotNone(response.json['items'])

    def launch_get_request(self, relative_endpoint):
        return self.app.get(
            f"{ROUTE_PREFIX}/{remove_prefix_slash(relative_endpoint)}",
            headers={"Origin": "map.geo.admin.ch"}
        )

    def test_checker(self):
        self.check_response_compliance(self.launch_get_request('/checker'))

    def test_icon_sets_list(self):
        self.check_response_compliance(self.launch_get_request('/sets'), is_list_endpoint=True)

    def test_icon_set_metadata(self):
        self.check_response_compliance(self.launch_get_request('/sets/default'))

    def test_icons_list(self):
        self.check_response_compliance(
            self.launch_get_request('/sets/default/icons'), is_list_endpoint=True
        )

    def test_icon_metadata(self):
        self.check_response_compliance(self.launch_get_request('/sets/default/icons/marker'))
