import logging
import logging.config
import os
from os import path

import yaml

from flask import jsonify
from flask import make_response

from app.settings import LOGGING_CFG
from app.settings import LOGS_DIR

logger = logging.getLogger(__name__)


def make_error_msg(code, msg):
    return make_response(jsonify({'success': False, 'error': {'code': code, 'message': msg}}), code)


def get_logging_cfg():
    cfg_file = os.getenv('LOGGING_CFG', 'logging-cfg-local.yml')
    print(f"LOGS_DIR is {LOGS_DIR}")
    print(f"LOGGING_CFG is {LOGGING_CFG}")

    config = {}
    with open(cfg_file, 'rt', encoding='utf-8') as fd:
        config = yaml.safe_load(path.expandvars(fd.read()))

    logger.debug('Load logging configuration from file %s', cfg_file)
    return config


def init_logging():
    config = get_logging_cfg()
    logging.config.dictConfig(config)
