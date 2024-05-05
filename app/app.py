from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.routes import api_bp
from views.routes import view_bp
from models.models import db
import logging
from config import Config

def create_app(config_class=Config):
    """
    Application factory function that creates and configures the Flask application.

    Args:
        config_class (class): The configuration class to use for application settings.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load configurations from the provided config class

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Register blueprints for API and views
    app.register_blueprint(api_bp)
    app.register_blueprint(view_bp)

    # Register custom error handlers
    register_error_handlers(app)

    # Setup logging
    setup_logging(app)

    with app.app_context():
        # Create database tables if they do not exist
        db.create_all()

    return app

def register_error_handlers(app):
    """
    Register error handlers for the application.

    Args:
        app (Flask): The application object to register error handlers on.
    """
    @app.errorhandler(404)
    def not_found_error(error):
        """Return a custom 404 error message."""
        return "Resource not found.", 404

    @app.errorhandler(500)
    def internal_error(error):
        """
        Handle 500 internal server errors with a rollback to save database integrity.
        """
        db.session.rollback()  # Roll back the current database session
        return "Internal server error.", 500

def setup_logging(app):
    """
    Set up logging configuration for the application.

    Args:
        app (Flask): The application object to configure logging for.
    """
    if not app.debug:
        # Log to a file if not in debug mode. Ensures all info level logs are written to 'app.log'.
        logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  # Run the application with debug enabled
