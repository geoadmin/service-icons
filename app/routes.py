from io import BytesIO
import os.path
from flask import Response
from flask import make_response
from flask import jsonify
from flask import abort
from flask import current_app as capp
from PIL import Image

from app import app
from app.helpers.check_functions import check_color_channels
from app.helpers.route import prefix_route
from app.helpers import make_error_msg

# add route prefix
app.route = prefix_route(app.route, '/v<int:ver>/color')


@app.route('/checker')
def checker_page(ver):
    """
    Just a route for the health check.
    :param ver: integer value of the service's version (inherited from prefix_route).
    :return: OK with a 200 status code or raise error in case of unsupported version.
    """
    if ver > 4:
        abort(make_error_msg(400, "unsupported version of service."))

    return make_response(jsonify({'success': True, 'message': 'OK'}))


@app.route('/<int:r>,<int:g>,<int:b>/<string:filename>', methods=['GET'])
def color(ver, r, g, b, filename):  # pylint: disable=invalid-name
    """
    This endpoint verifies the parameters of the request.
    BadRequests errors will be raised in case of not properly defined parameters.
    If all parameters are well defined, the colored image (symbol) is returned.
    :param ver: integer value of the service's version (inherited from prefix_route).
    :param r: integer value in the range between 0 and 255 for the red channel.
    :param g: integer value in the range between 0 and 255 for the green channel.
    :param b: integer value in the range between 0 and 255 for the blue channel.
    :param filename: name of the file containing the image/symbol to be colored.
    :return:
    """
    if ver > 4:
        abort(make_error_msg(400, "unsupported version of service."))

    r, g, b = check_color_channels(r, g, b)

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/images/', filename))
    if not os.path.isfile(path):
        capp.logger.error("The image to colorize doesn\'t exist.")
        abort(make_error_msg(400, "The image to colorize doesn\'t exist."))

    with Image.open(path) as mask:
        if mask.mode == 'P':
            mask = mask.convert('RGBA')
        img = Image.composite(Image.new("RGB", mask.size, (r, g, b)), mask, mask)
        output = BytesIO()
        img.save(output, format='PNG')
        img.close()

    return Response(output.getvalue(), mimetype='image/png')
