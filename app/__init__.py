from flask import Flask
from app.middleware import ReverseProxied

# Standard Flask application initialisation

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app, script_name='/')


from app import routes


def main():

    app.run()


if __name__ == '__main__':
    """
    Entrypoint for the application. At the moment, we do nothing specific, but there might be preparatory steps in the 
    future
    """
    main()
