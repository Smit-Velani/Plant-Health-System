"""
app/__init__.py — Flask application factory
"""

from flask import Flask
from app.config import SECRET_KEY, UPLOAD_FOLDER, MAX_CONTENT_LENGTH


def create_app():
    app = Flask(__name__,
                template_folder="../templates",
                static_folder="../static")

    # Config
    app.config["SECRET_KEY"]           = SECRET_KEY
    app.config["UPLOAD_FOLDER"]        = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"]   = MAX_CONTENT_LENGTH

    # Lazy-load predictor (avoid import-time TF load)
    from app.model.predictor import PlantDiseasePredictor
    app.config["PREDICTOR"] = PlantDiseasePredictor()

    # Register blueprints
    from app.routes.api import api
    app.register_blueprint(api)

    return app
