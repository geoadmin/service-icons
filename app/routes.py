import logging
from io import BytesIO

from PIL import Image

from flask import Response
from flask import jsonify
from flask import make_response

from app import app
from app.helpers.check_functions import check_color_channels
from app.helpers.check_functions import get_and_check_icon
from app.helpers.check_functions import get_and_check_icon_set
from app.helpers.icons import get_all_icon_sets
from app.helpers.route import prefix_route
from app.settings import DEFAULT_COLOR
from app.settings import ROUTE_PREFIX
from app.version import APP_VERSION

logger = logging.getLogger(__name__)

# add route prefix
app.route = prefix_route(app.route, ROUTE_PREFIX)


@app.route('/checker')
def checker_page():
    """
    Just a route for the health check.
    :return: OK with a 200 status code or raise error in case of unsupported version.
    """
    return make_response(jsonify({'success': True, 'message': 'OK', 'version': APP_VERSION}))


@app.route('', methods=['GET'])
@app.route('/', methods=['GET'])
def all_icon_sets():
    return make_response(jsonify({"success": True, "items": get_all_icon_sets()}))


@app.route('/<string:icon_set_name>', methods=['GET'])
def icon_set_metadata(icon_set_name):
    icon_set = get_and_check_icon_set(icon_set_name)
    return make_response(jsonify(icon_set))


@app.route('/<string:icon_set_name>/icons', methods=['GET'])
def icons_from_icon_set(icon_set_name):
    icon_set = get_and_check_icon_set(icon_set_name)
    return make_response(jsonify({"success": True, "items": icon_set.get_all_icons()}))


@app.route('/<string:icon_set_name>/icon/<string:icon_name>', methods=['GET'])
def icon_metadata(icon_set_name, icon_name):
    icon_set = get_and_check_icon_set(icon_set_name)
    icon = get_and_check_icon(icon_set, icon_name)
    return make_response(jsonify(icon))


@app.route('/<string:icon_set_name>/icon/<string:icon_name>.png', methods=['GET'])
@app.route(
    '/<string:icon_set_name>/icon/<string:icon_name>-<int:red>,<int:green>,<int:blue>.png',
    methods=['GET']
)
@app.route('/<string:icon_set_name>/icon/<string:icon_name>@<string:scale>.png', methods=['GET'])
@app.route(
    '/<string:icon_set_name>/icon/<string:icon_name>@<string:scale>'
    '-<int:red>,<int:green>,<int:blue>.png',
    methods=['GET']
)
def colorized_icon(
    icon_set_name,
    icon_name,
    scale='1x',
    red=DEFAULT_COLOR['r'],
    green=DEFAULT_COLOR['g'],
    blue=DEFAULT_COLOR['b']
):
    red, green, blue = check_color_channels(red, green, blue)
    icon_set = get_and_check_icon_set(icon_set_name)
    icon = get_and_check_icon(icon_set, icon_name)
    scale_factor = 1
    if scale == '2x':
        scale_factor = 2
    elif scale in ('0.5x', '.5x'):
        scale_factor = 0.5

    with open(icon.get_icon_filepath(), 'rb') as fd:
        image = Image.open(fd)
        if image.mode == 'P':
            image = image.convert('RGBA')
        new_size = int(48 * scale_factor)
        if new_size != icon_set.get_default_pixel_size():
            image = image.resize((new_size, new_size))
        if icon_set.colorable:
            image = Image.composite(Image.new("RGB", image.size, (red, green, blue)), image, image)
        output = BytesIO()
        image.save(output, format='PNG')

        return Response(output.getvalue(), mimetype='image/png')
