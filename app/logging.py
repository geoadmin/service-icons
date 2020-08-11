import json
import logging
from datetime import datetime

from flask import has_request_context
from flask import request
from flask.logging import default_handler


class JsonFormatter(logging.Formatter):

    def format(self, record):
        msg_obj = {
            'time': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelno,
            'levelname': record.levelname,
            'application': 'service-color',
            'name': record.name,
            'message': record.msg % record.args,
            'request': None
        }
        if has_request_context():
            msg_obj.update({'request': {'url': request.url, 'data': request.get_json()}})
        return json.dumps(msg_obj)


default_handler.setFormatter(JsonFormatter())

# Uses the default handler for all libraries (e.g. werkzeug)
root = logging.getLogger()
root.addHandler(default_handler)
