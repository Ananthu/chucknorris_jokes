from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.routes import api_bp
from views.routes import view_bp
from models.models import db
import logging
from config import Config


def create_app(config_class=Config):
    """
    Application factory function that creates and configures the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load configurations from a config class

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Register blueprints for API and views
    app.register_blueprint(api_bp)
    app.register_blueprint(view_bp)

    # Error handlers
    register_error_handlers(app)

    # Initialize logging
    setup_logging(app)

    with app.app_context():
        # Create all database tables based on the models
        db.create_all()

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return "Resource not found.", 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Roll back in case of failure
        return "Internal server error.", 500

def setup_logging(app):
    if not app.debug:
        # Configure logging to output errors to a log file
        logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                            format='%(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
