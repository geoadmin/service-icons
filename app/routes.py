from io import BytesIO
import os.path
from flask import Response, make_response, jsonify, abort
from PIL import Image
from app import app
from app.helpers.check_functions import check_color_channels
from app.helpers.route import prefix_route
from app.helpers import make_error_msg

# add route prefix
app.route = prefix_route(app.route, '/v4/color/')


@app.route('/checker')
def checker_page():
    """
    Just a route for the health check
    :return: OK with a 200 status code
    """
    return make_response(jsonify({'success': True, 'message': 'OK'}))


@app.route('/<int:r>,<int:g>,<int:b>/<string:filename>', methods=['GET'])
def color(r, g, b, filename): # pylint: disable=invalid-name
    """
    This endpoint verifies the parameters of the request.
    BadRequests errors will be raised in case of not properly defined parameters.
    If all parameters are well defined, the colored image (symbol) is returned.
    :param r: integer value in the range between 0 and 255 for the red channel
    :param g: integer value in the range between 0 and 255 for the green channel
    :param b: integer value in the range between 0 and 255 for the blue channel
    :param filename: name of the file containing the image/symbol to be colored
    :return:
    """
    r, g, b = check_color_channels(r, g, b)

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/images/', filename))
    if not os.path.isfile(path):
        abort(make_error_msg(400, "The image to colorize doesn\'t exist"))

    with Image.open(path) as mask:
        if mask.mode == 'P':
            mask = mask.convert('RGBA')
        img = Image.composite(Image.new("RGB", mask.size, (r, g, b)), mask, mask)
        output = BytesIO()
        img.save(output, format='PNG')
        img.close()

    return Response(output.getvalue(), mimetype='image/png')
