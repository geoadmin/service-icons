import json
import os
from app.settings import JSON_FOLDER

def get_icon_translation(icon_name='', icon_set=''):
    path = os.path.abspath(os.path.join(JSON_FOLDER, icon_set + '_dictionary.json'))
    if(not(os.path.isfile(path))):
        return "false"

    with open(path) as f:
        df = json.load(f)

    id = icon_name[0:3]
    icon_translation = df['ICON_'+id]
    return icon_translation
