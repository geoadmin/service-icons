import json

from app.icon import Icon
from app.icon_set import IconSet


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, (Icon, IconSet)):
            return o.serialize()
        return super().default(o)
