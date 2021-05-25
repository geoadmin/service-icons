import os

ALLOWED_DOMAINS = [
    r'.*\.geo\.admin\.ch',
    r'.*bgdi\.ch',
    r'.*\.swisstopo\.cloud',
]

ALLOWED_DOMAINS_PATTERN = '({})'.format('|'.join(ALLOWED_DOMAINS))


ROUTE_PREFIX = '/v4/iconsets'
IMAGE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/images/'))

COLORABLE_ICON_SETS = ['default']
DEFAULT_COLOR = {"r": 255, "g": 0, "b": 0}
