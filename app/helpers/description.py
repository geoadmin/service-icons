import json
import os

from app.settings import DESCRIPTION_FOLDER


def get_icon_set_description(icon_set=''):
    '''
    Return json containing the description in all available languages for all icons of the
    provided icon set
    '''
    path = find_descripton_file(icon_set)
    if not os.path.isfile(path):
        return None

    with open(path, encoding='utf-8') as f:
        icon_set_descriptions = json.load(f)

    return icon_set_descriptions


def get_icon_description(icon_name='', icon_set=''):
    '''
    Return json containing the description in all available languages for the specified icon of the
    provided icon set
    '''
    path = find_descripton_file(icon_set)
    if not os.path.isfile(path):
        return None

    with open(path, encoding='utf-8') as f:
        df = json.load(f)

    icon_description = df[icon_name]
    return icon_description


def find_descripton_file(icon_set):
    '''
    Return file path of description file if it exists
    '''
    path = os.path.abspath(os.path.join(DESCRIPTION_FOLDER, icon_set)) + '-dictionary.json'
    if os.path.isfile(path):
        return path
    return False
