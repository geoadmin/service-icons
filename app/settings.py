import os
from pathlib import Path

from app.helpers.icons import split_and_clean_string

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
ENV_FILE = os.getenv('ENV_FILE', f'{BASE_DIR}/.env.local')
if ENV_FILE and Path(ENV_FILE).exists():
    from dotenv import load_dotenv

    print(f"Running locally hence injecting env vars from {ENV_FILE}")
    load_dotenv(ENV_FILE, override=True, verbose=True)

IMAGE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/images/'))
DESCRIPTION_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../metadata/description/')
)

COLORABLE_ICON_SETS = ['default']

UNLISTED_ICON_SETS = split_and_clean_string(os.environ.get('UNLISTED_ICON_SETS', ''))

ICON_SET_LANGUAGE = {'babs-v2-de': 'de', 'babs-v2-fr': 'fr', 'babs-v2-it': 'it'}
DEFAULT_COLOR = {"r": '255', "g": '0', "b": '0'}
DEFAULT_ICON_SIZE = 48
TRAP_HTTP_EXCEPTIONS = True
LOGS_DIR = os.getenv('LOGS_DIR', str(BASE_DIR / 'logs'))
os.environ['LOGS_DIR'] = LOGS_DIR  # Set default if not set
LOGGING_CFG = os.getenv('LOGGING_CFG', 'logging-cfg-local.yml')

GUNICORN_KEEPALIVE = int(os.getenv('GUNICORN_KEEPALIVE', '2'))

# Definition of the allowed domains for CORS implementation
ALLOWED_DOMAINS = os.getenv('ALLOWED_DOMAINS', r'.*').split(',')
CACHE_CONTROL = os.getenv('CACHE_CONTROL', 'public, max-age=86400')
CACHE_CONTROL_4XX = os.getenv('CACHE_CONTROL_4XX', 'public, max-age=3600')
