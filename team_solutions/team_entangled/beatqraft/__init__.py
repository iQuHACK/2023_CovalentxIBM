from flask import Flask, session, request, g
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        from . import routes
        # from .assets import compile_static_assets

        # Register Blueprints
        app.register_blueprint(routes.main_bp)

        return app

