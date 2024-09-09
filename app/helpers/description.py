import json
import logging
import os

from flask import abort

from app.settings import DESCRIPTION_FOLDER

logger = logging.getLogger(__name__)


def get_icon_description(icon_name='', icon_set=''):
    '''
    Return json containing the description in all available languages for an icon in the specified
    icon set
    '''
    path = find_descripton_file(icon_set)
    if not os.path.isfile(path):
        return None

    with open(path, encoding='utf-8') as f:
        df = json.load(f)

    try:
        icon_description = df[icon_name]
    except KeyError:
        logger.error("Description for icon not found: %s", icon_name)
        abort(404, "Description for icon not found")

    return icon_description


def find_descripton_file(icon_set):
    '''
    Return file path of description file if it exists or False in case it doesn't
    '''
    path = os.path.abspath(os.path.join(DESCRIPTION_FOLDER, icon_set)) + '-dictionary.json'
    if os.path.isfile(path):
        return path
    return False
