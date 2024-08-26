import json
import os

from app.settings import JSON_FOLDER


def get_icon_set_description(icon_set=''):
    path = os.path.abspath(os.path.join(JSON_FOLDER, icon_set + '-dictionary.json'))
    if not os.path.isfile(path):
        return None

    with open(path, encoding='utf-8') as f:
        df = json.load(f)

    return df


def get_icon_description(icon_name='', icon_set=''):
    path = os.path.abspath(os.path.join(JSON_FOLDER, icon_set + '-dictionary.json'))
    if not os.path.isfile(path):
        return False

    with open(path, encoding='utf-8') as f:
        df = json.load(f)

    icon_description = df[icon_name]
    return icon_description
