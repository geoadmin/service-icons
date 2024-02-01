import json
import os

from app.settings import JSON_FOLDER


def get_icon_set_translation(icon_set=''):
    path = os.path.abspath(os.path.join(JSON_FOLDER, icon_set + '_dictionary.json'))
    if not os.path.isfile(path):
        return False
    return True


def get_icon_translation(icon_name='', icon_set=''):
    path = os.path.abspath(os.path.join(JSON_FOLDER, icon_set + '_dictionary.json'))
    if not os.path.isfile(path):
        return False

    with open(path, encoding='utf-8') as f:
        df = json.load(f)

    icon_translation = df['ICON_' + icon_name[0:3]]
    return icon_translation
