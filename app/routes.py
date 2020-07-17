import os.path
import six # for compatibility Python 2 / 3

from PIL import Image
# replaced by wekrzeug.exceptions:
# from pyramid.httpexceptions import HTTPBadRequest and other flask stuff
# from pyramid.view import view_config
# from pyramid.response import Response

# for raising BadRequest error messages without using pyramid
from werkzeug.exceptions import BadRequest
from flask import send_file, Response

# Python2/3 compatibility
if six.PY3:
    from io import BytesIO
else:
    from StringIO import StringIO


from app import app


# not sure if this is needed, but just in case:
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
    BadRequests errors will be raised in case of not properly defined After that the service-color is called and the colored
    image (symbol) is returned.

    :param r: integer value in the range between 0 and 255 for the red channel
    :param g: integer value in the range between 0 and 255 for the green channel
    :param b: integer value in the range between 0 and 255 for the blue channel
    :param filename: name of the file containing the image/symbol to be colored
    :return:
    """

    # formerly it was only tested if r, g and b are integers. I extended
    # that test to check, if they are in the range of 0 to 255.
    # at least according to: https://pillow.readthedocs.io/en/stable/reference/ImageColor.html
    # color values should be integers between 0 and 255.

    if r.isdigit() is False:
        raise BadRequest('The red channel must be an integer value.')
    elif not (0 <= int(r) <=255):
        raise BadRequest('The red channel must be an integer value in the range of 0 to 255.')

    if g.isdigit() is False:
        raise BadRequest('The green channel must be an integer value.')
    elif not (0 <= int(g) <=255):
        raise BadRequest('The green channel must be an integer value in the range of 0 to 255.')

    if b.isdigit() is False:
        raise BadRequest('The blue channel must be an integer value.')
    elif not (0 <= int(b) <=255):
        raise BadRequest('The blue channel must be an integer value in the range of 0 to 255.')

    r = int(r)
    g = int(g)
    b = int(b)

    image_name = self.request.matchdict['filename']
    path = os.path.join(self.request.registry.settings['install_directory'], 'chsdi/static/images/maki/', image_name)
    if not os.path.isfile(path):
        raise BadRequest('The image to color doesn\'t exist')

    mask = Image.open(path)
    # This auto conversion gives really bad results
    if mask.mode == 'P':
        mask = mask.convert('RGBA')
    img = Image.composite(Image.new("RGB", mask.size, (r, g, b)), mask, mask)
    if six.PY3:
        output = BytesIO()
    else:
        output = StringIO()
    img.save(output, format='PNG')
    send_file(output.getvalue(), mimetype='image/png')  # or better create a response object and return that?

