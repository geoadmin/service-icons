import os.path
# using werkzeug.exceptions in order to get rid of pyramid
# from pyramid.httpexceptions import HTTPBadRequest and other flask stuff
# from pyramid.view import view_config
# from pyramid.response import Response
from flask import Response
import six  # for compatibility Python 2 / 3
from PIL import Image
from app import app
from app.helpers import check_color_channels
from app.helpers import check_path

# Python2/3 compatibility
if six.PY3:
    from io import BytesIO
else:
    from StringIO import StringIO


@app.route('/checker')
@app.route('/checker/')
def checker_page():
    """
    Just a route for the health check
    :return: OK with a 200 status code
    """
    return "OK", 200


@app.route('/color/<r>,<g>,<b>/<filename>/', methods=['GET'])
@app.route('/color/<r>,<g>,<b>/<filename>', methods=['GET'])
def color(r, g, b, filename):
    """
    This endpoint verifies the parameters of the request.
    BadRequests errors will be raised in case of not properly defined parameters.
    If all parameters are well defined the colored image (symbol) is returned.
    :param r: integer value in the range between 0 and 255 for the red channel
    :param g: integer value in the range between 0 and 255 for the green channel
    :param b: integer value in the range between 0 and 255 for the blue channel
    :param filename: name of the file containing the image/symbol to be colored
    :return:
    """
    check_color_channels(r, g, b)
    r = int(r)
    g = int(g)
    b = int(b)

    # the images are currently stored in a subfolder calles "maki".
    # is it necessary to keep this subfolder, or is ../static/images/ ok?
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/images/', filename))

    check_path(path)

    mask = Image.open(path)

    if mask.mode == 'P':
        mask = mask.convert('RGBA')
    img = Image.composite(Image.new("RGB", mask.size, (r, g, b)), mask, mask)
    if six.PY3:
        output = BytesIO()
    else:
        output = StringIO()
    img.save(output, format='PNG')

    return Response(output.getvalue(), mimetype='image/png')
    