import json
import os

from app.settings import DESCRIPTION_FOLDER
from tests.unit_tests.base_test import ServiceIconsUnitTests


def validate_json(json_file):
    try:
        json.loads(json_file)
    except ValueError as err:
        return False
    return True


class IconsTests(ServiceIconsUnitTests):

    def test_validate_json_description_files(self):
        files = list(os.listdir(DESCRIPTION_FOLDER))
        for file in files:
            for root, dirs, files in os.walk(os.path.join(DESCRIPTION_FOLDER)):
                for name in files:
                    p = os.path.join(root, name)
                    with open(p, encoding='utf-8') as f:
                        json_file = f.read()
                    self.assertTrue(
                        validate_json(json_file), "validation failed of json file: " + file
                    )
