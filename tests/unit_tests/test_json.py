import json
import os

from app.settings import JSON_FOLDER
from tests.unit_tests.base_test import ServiceIconsUnitTests


def validate_json(json_file):
    try:
        json.loads(json_file)
    except ValueError as err:
        return False
    return True


class IconsTests(ServiceIconsUnitTests):

    def test_json(self):
        path = os.path.abspath(os.path.join(JSON_FOLDER, 'babs2_dictionary.json'))
        self.assertTrue(os.path.exists(path), "babs2 json file doesn't exist")

        for root, dirs, files in os.walk(os.path.join(JSON_FOLDER)):
            for name in files:
                p = os.path.join(root, name)
                with open(p, encoding='utf-8') as f:
                    json_file = f.read()
                self.assertTrue(validate_json(json_file), "json file validation failed")
