from flask import Flask

def init_app():
    """Create Flask application."""
    app = Flask(__name__)

    with app.app_context():
        # Import parts of our application
        from . import routes

        # Register Blueprints
        app.register_blueprint(routes.bp)

        return app
