from flask import url_for

from tests.unit_tests.base_test import ServiceIconsUnitTests


class CheckerTests(ServiceIconsUnitTests):

    def check_response_compliance(self, response, is_list_endpoint=False, is_checker=False):
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        if not is_checker:
            self.assertCors(response)
            self.assertIn('Cache-Control', response.headers)
            self.assertIn('max-age=', response.headers['Cache-Control'])
        self.assertTrue('success' in response.json)
        self.assertTrue(response.json['success'])
        if is_list_endpoint:
            self.assertTrue('items' in response.json)
            self.assertIsNotNone(response.json['items'])

    def test_checker(self):
        self.check_response_compliance(
            self.app.get(url_for('checker'), headers=self.default_header), is_checker=True
        )

    def test_icon_sets_list(self):
        self.check_response_compliance(
            self.app.get(url_for('all_icon_sets'), headers=self.default_header),
            is_list_endpoint=True
        )

    def test_icon_set_metadata(self):
        self.check_response_compliance(
            self.app.get(
                url_for('icon_set_metadata', icon_set_name='default'), headers=self.default_header
            )
        )

    def test_icon_set_description(self):
        self.check_response_compliance(
            self.app.get(
                url_for('description_from_icon_set', icon_set_name='babs-I'),
                headers=self.default_header
            )
        )

    def test_icons_list(self):
        self.check_response_compliance(
            self.app.get(
                url_for('icons_from_icon_set', icon_set_name='default'),
                headers=self.default_header
            ),
            is_list_endpoint=True
        )

    def test_icon_metadata(self):
        self.check_response_compliance(
            self.app.get(
                url_for('icon_metadata', icon_set_name='default', icon_name='001-marker'),
                headers=self.default_header
            )
        )
