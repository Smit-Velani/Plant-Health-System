"""
routes/api.py — Flask route definitions
"""

import os
import uuid
from flask import Blueprint, request, jsonify, render_template, current_app
from werkzeug.utils import secure_filename
from app.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

api = Blueprint("api", __name__)


def _allowed(filename: str) -> bool:
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Pages ──────────────────────────────────────────────────────────────────────

@api.route("/")
def index():
    return render_template("index.html")


# ── Prediction endpoint ────────────────────────────────────────────────────────

@api.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not _allowed(file.filename):
        return jsonify({"error": "Invalid file type. Use PNG or JPG."}), 400

    # Save upload
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    ext      = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Predict
    try:
        predictor = current_app.config["PREDICTOR"]
        result    = predictor.predict(filepath)
        result["image_url"] = f"/static/uploads/{filename}"
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Health check ───────────────────────────────────────────────────────────────

@api.route("/health")
def health():
    return jsonify({"status": "ok", "model": "MobileNetV2 — PlantVillage"})
