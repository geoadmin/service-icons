import logging
from io import BytesIO

from PIL import Image

from flask import Response
from flask import jsonify
from flask import make_response

from app import app
from app.helpers.check_functions import check_color_channels
from app.helpers.check_functions import check_scale
from app.helpers.check_functions import get_and_check_icon
from app.helpers.check_functions import get_and_check_icon_set
from app.icon import Icon
from app.icon_set import IconSet
from app.icon_set import get_all_icon_sets
from app.settings import DEFAULT_COLOR
from app.version import APP_VERSION

logger = logging.getLogger(__name__)


def make_api_compliant_response(response_object):
    """
    Making sure our responses are compliant with
    https://github.com/geoadmin/doc-guidelines/blob/master/API.md
    """
    if isinstance(response_object, (Icon, IconSet)):
        return make_response(jsonify({'success': True, **response_object.serialize()}))
    if all(isinstance(r, (Icon, IconSet)) for r in response_object):
        return make_response(
            jsonify({
                'success': True, "items": [r.serialize() for r in response_object]
            })
        )
    if isinstance(response_object, list):
        return make_response(jsonify({'success': True, "items": response_object}))
    return make_response(jsonify({'success': True, **response_object}))


@app.route('/checker', methods=['GET'])
def checker():
    """
    Just a route for the health check.
    :return: OK with a 200 status code or raise error in case of unsupported version.
    """
    return make_api_compliant_response({'message': 'OK', 'version': APP_VERSION})


@app.route('/sets', methods=['GET'])
def all_icon_sets():
    return make_api_compliant_response(get_all_icon_sets())


@app.route('/sets/<string:icon_set_name>', methods=['GET'])
def icon_set_metadata(icon_set_name):
    return make_api_compliant_response(get_and_check_icon_set(icon_set_name))


@app.route('/sets/<string:icon_set_name>/icons', methods=['GET'])
def icons_from_icon_set(icon_set_name):
    icon_set = get_and_check_icon_set(icon_set_name)
    return make_api_compliant_response(icon_set.get_all_icons())


@app.route('/sets/<string:icon_set_name>/icons/<string:icon_name>', methods=['GET'])
def icon_metadata(icon_set_name, icon_name):
    icon_set = get_and_check_icon_set(icon_set_name)
    icon = get_and_check_icon(icon_set, icon_name)
    return make_api_compliant_response(icon)


@app.route('/sets/<icon_set_name>/icons/<icon_name>.png',)
@app.route('/sets/<icon_set_name>/icons/<icon_name>-<red>,<green>,<blue>.png',)
@app.route('/sets/<icon_set_name>/icons/<icon_name>@<scale>.png',)
@app.route('/sets/<icon_set_name>/icons/<icon_name>@<scale>-<red>,<green>,<blue>.png',)
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
    scale = check_scale(scale)

    with open(icon.get_icon_filepath(), 'rb') as fd:
        image = Image.open(fd)
        if image.mode == 'P':
            image = image.convert('RGBA')
        if scale != 1:
            new_size = map(lambda s: int(s * scale), icon.get_size())
            image = image.resize(new_size)
        if icon_set.colorable:
            image = Image.composite(Image.new("RGB", image.size, (red, green, blue)), image, image)
        output = BytesIO()
        image.save(output, format='PNG')

        return Response(output.getvalue(), mimetype='image/png')
