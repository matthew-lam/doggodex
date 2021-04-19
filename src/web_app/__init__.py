from flask import Flask
from .config import Config

def init_app():
    """Create Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    print('configs')
    print(Config)
    print(app.config)

    with app.app_context():
        # Import parts of our application
        from . import routes

        # Register Blueprints
        app.register_blueprint(routes.bp)

        return app
