import os

from gunicorn.app.base import BaseApplication

from app import app as application
from app.helpers import get_logging_cfg
from app.settings import GUNICORN_KEEPALIVE


class StandaloneApplication(BaseApplication):  # pylint: disable=abstract-method

    def __init__(self, app, options=None):  # pylint: disable=redefined-outer-name
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key,
            value in self.options.items() if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# We use the port 5000 as default, otherwise we set the HTTP_PORT env variable within the container.
if __name__ == '__main__':
    HTTP_PORT = str(os.environ.get('HTTP_PORT', "5000"))
    # Bind to 0.0.0.0 to let your app listen to all network interfaces.
    options = {
        'bind': f"0.0.0.0:{HTTP_PORT}",
        'worker_class': 'gevent',
        'worker_tmp_dir': os.getenv("GUNICORN_TMPFS_DIR", None),
        'workers': int(os.getenv('WSGI_WORKERS',
                                 '2')),  # scaling horizontally is left to Kubernetes
        'timeout': int(os.getenv('WSGI_TIMEOUT', '5')),
        'keepalive': GUNICORN_KEEPALIVE,
        'logconfig_dict': get_logging_cfg(),
        'forwarded_allow_ips': os.getenv('FORWARED_ALLOW_IPS', '*'),
        'secure_scheme_headers': {
            os.getenv('FORWARDED_PROTO_HEADER_NAME', 'X-Forwarded-Proto').upper(): 'https'
        }
    }
    StandaloneApplication(application, options).run()
