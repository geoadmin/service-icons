import logging
import os.path
from io import BytesIO

from PIL import Image

from flask import Response
from flask import abort
from flask import jsonify
from flask import make_response

from app import app
from app.helpers import make_error_msg
from app.helpers.check_functions import check_color_channels
from app.helpers.icons import get_all_icons
from app.helpers.icons import get_icon_filepath
from app.helpers.route import prefix_route
from app.settings import ROUTE_PREFIX
from app.version import APP_VERSION

logger = logging.getLogger(__name__)

# add route prefix
app.route = prefix_route(app.route, ROUTE_PREFIX)


@app.route('/checker')
def checker_page():
    """
    Just a route for the health check.
    :param ver: integer value of the service's version (inherited from prefix_route).
    :return: OK with a 200 status code or raise error in case of unsupported version.
    """
    return make_response(jsonify({'success': True, 'message': 'OK', 'version': APP_VERSION}))


@app.route('/all', methods=['GET'])
def all_images():
    """
    List all available icons and return them as a JSON array
    When available icons can be colorized, it will output URLs with the default color red
    """
    return make_response(jsonify(get_all_icons()))


@app.route('/<string:category>/<int:red>,<int:green>,<int:blue>/<string:filename>', methods=['GET'])
def colorized_icon(category, red, green, blue, filename):
    """
    This endpoint verifies the parameters of the request.
    BadRequests errors will be raised in case of not properly defined parameters.
    If all parameters are well defined, the colored image (symbol) is returned.
    :param category: name of the icon's category (default is used if not defined)
    :param red: integer value in the range between 0 and 255 for the red channel.
    :param green: integer value in the range between 0 and 255 for the green channel.
    :param blue: integer value in the range between 0 and 255 for the blue channel.
    :param filename: name of the file containing the image/symbol to be colored.
    :return:
    """
    logger.debug('GET color (%d, %d, %d) for %s', red, green, blue, filename)

    red, green, blue = check_color_channels(red, green, blue)

    path = get_icon_filepath(category, filename)
    if not os.path.isfile(path):
        logger.error("The image to colorize doesn't exist.")
        abort(make_error_msg(400, "The image to colorize doesn't exist."))

    with Image.open(path) as mask:
        if mask.mode == 'P':
            mask = mask.convert('RGBA')
        img = Image.composite(Image.new("RGB", mask.size, (red, green, blue)), mask, mask)
        output = BytesIO()
        img.save(output, format='PNG')
        img.close()

    return Response(output.getvalue(), mimetype='image/png')
