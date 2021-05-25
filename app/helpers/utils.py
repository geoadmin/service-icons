import logging
import logging.config
import os

import yaml

from flask import jsonify
from flask import make_response

logger = logging.getLogger(__name__)


def make_error_msg(code, msg):
    return make_response(jsonify({'success': False, 'error': {'code': code, 'message': msg}}), code)


def get_logging_cfg():
    cfg_file = os.getenv('LOGGING_CFG', 'logging-cfg-local.yml')

    config = {}
    with open(cfg_file, 'rt') as fd:
        config = yaml.safe_load(fd.read())

    logger.debug('Load logging configuration from file %s', cfg_file)
    return config


def init_logging():
    config = get_logging_cfg()
    logging.config.dictConfig(config)
