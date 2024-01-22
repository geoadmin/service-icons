import json
import os

from tests.unit_tests.base_test import ServiceIconsUnitTests

from app.settings import JSON_FOLDER

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

class IconsTests(ServiceIconsUnitTests):

    def test_json(self):
        path = os.path.abspath(os.path.join(JSON_FOLDER, 'babs2_dictionary.json'))
        self.assertTrue(os.path.exists(path),"babs2 json file doesn't exist")

        for root, dirs, files in os.walk(os.path.join(JSON_FOLDER)):
            for name in files:
                p = os.path.join(root, name)
                with open(p) as f:
                    json_file = f.read()
                self.assertTrue(validateJSON(json_file),"json file validation failed")

