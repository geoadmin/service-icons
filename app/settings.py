import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
ENV_FILE = os.getenv('ENV_FILE', f'{BASE_DIR}/.env.local')
if ENV_FILE and Path(ENV_FILE).exists():
    from dotenv import load_dotenv

    print(f"Running locally hence injecting env vars from {ENV_FILE}")
    load_dotenv(ENV_FILE, override=True, verbose=True)

IMAGE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/images/'))

COLORABLE_ICON_SETS = ['default']
DEFAULT_COLOR = {"r": '255', "g": '0', "b": '0'}
TRAP_HTTP_EXCEPTIONS = True
LOGS_DIR = os.getenv('LOGS_DIR', str(BASE_DIR / 'logs'))
os.environ['LOGS_DIR'] = LOGS_DIR  # Set default if not set
LOGGING_CFG = os.getenv('LOGGING_CFG', 'logging-cfg-local.yml')

# Definition of the allowed domains for CORS implementation
ALLOWED_DOMAINS = os.getenv('ALLOWED_DOMAINS', r'.*').split(',')
ALLOWED_DOMAINS_PATTERN = f"({'|'.join(ALLOWED_DOMAINS)})"
CACHE_CONTROL = os.getenv('CACHE_CONTROL', 'public, max-age=86400')
CACHE_CONTROL_4XX = os.getenv('CACHE_CONTROL_4XX', 'public, max-age=3600')
