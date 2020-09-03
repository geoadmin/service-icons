import logging

from flask import jsonify
from flask import make_response

from app import app

logger = logging.getLogger(__name__)


@app.route('/checker', methods=['GET'])
def check():
    return make_response(jsonify({'success': True, 'message': 'OK'}))
