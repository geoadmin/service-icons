import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
ENV_FILE = os.getenv('ENV_FILE', f'{BASE_DIR}/.env.local')
if ENV_FILE and Path(ENV_FILE).exists():
    from dotenv import load_dotenv

    print(f"Running locally hence injecting env vars from {ENV_FILE}")
    load_dotenv(ENV_FILE, override=True, verbose=True)

ROUTE_PREFIX = '/v4/icons'
IMAGE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/images/'))

COLORABLE_ICON_SETS = ['default']
DEFAULT_COLOR = {"r": 255, "g": 0, "b": 0}
TRAP_HTTP_EXCEPTIONS = True

# Definition of the allowed domains for CORS implementation
ALLOWED_DOMAINS_STRING = os.getenv(
    'ALLOWED_DOMAINS', r'.*\.geo\.admin\.ch,.*\.bgdi\.ch,.*\.swisstopo\.cloud'
)
ALLOWED_DOMAINS = ALLOWED_DOMAINS_STRING.split(',')
