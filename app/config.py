"""
config.py — Central configuration for Plant Health Prediction System
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ── Flask ──────────────────────────────────────────────────────────────────────
SECRET_KEY       = os.environ.get("SECRET_KEY", "plant-health-secret-key-2025")
DEBUG            = os.environ.get("DEBUG", "True") == "True"
HOST             = "0.0.0.0"
PORT             = 5000

# ── Upload ─────────────────────────────────────────────────────────────────────
UPLOAD_FOLDER    = os.path.join(BASE_DIR, "..", "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # 16 MB

# ── Model ──────────────────────────────────────────────────────────────────────
MODEL_PATH       = os.path.join(BASE_DIR, "..", "model", "plant_model.h5")
IMG_SIZE         = (224, 224)
CONFIDENCE_THRESHOLD = 0.40

# ── Plant Disease Classes (PlantVillage dataset — 19 classes) ──────────────────
CLASSES = [
    "Pepper — Bacterial Spot",
    "Pepper — Healthy",
    "Potato — Early Blight",
    "Potato — Late Blight",
    "Potato — Healthy",
    "Tomato — Bacterial Spot",
    "Tomato — Early Blight",
    "Tomato — Late Blight",
    "Tomato — Leaf Mold",
    "Tomato — Septoria Leaf Spot",
    "Tomato — Spider Mites",
    "Tomato — Target Spot",
    "Tomato — Yellow Leaf Curl Virus",
    "Tomato — Mosaic Virus",
    "Tomato — Healthy",
]

# ── Disease Info ───────────────────────────────────────────────────────────────
DISEASE_INFO = {
    "Healthy": {
        "status"    : "healthy",
        "severity"  : "None",
        "treatment" : "No treatment needed. Continue regular care.",
        "prevention": "Maintain good watering schedule and sunlight.",
    },
    "Apple Scab": {
        "status"    : "diseased",
        "severity"  : "Moderate",
        "treatment" : "Apply fungicides containing myclobutanil or captan.",
        "prevention": "Remove fallen leaves, ensure good air circulation.",
    },
    "Black Rot": {
        "status"    : "diseased",
        "severity"  : "High",
        "treatment" : "Prune infected areas, apply copper-based fungicide.",
        "prevention": "Avoid overhead watering, sanitize pruning tools.",
    },
    "Cedar Apple Rust": {
        "status"    : "diseased",
        "severity"  : "Moderate",
        "treatment" : "Apply preventive fungicide sprays in spring.",
        "prevention": "Remove nearby cedar trees, use resistant varieties.",
    },
    "Common Rust": {
        "status"    : "diseased",
        "severity"  : "Moderate",
        "treatment" : "Apply fungicides with azoxystrobin or propiconazole.",
        "prevention": "Plant rust-resistant hybrids, monitor humidity.",
    },
    "Early Blight": {
        "status"    : "diseased",
        "severity"  : "Moderate",
        "treatment" : "Apply chlorothalonil or copper fungicide weekly.",
        "prevention": "Rotate crops, avoid overhead watering.",
    },
    "Late Blight": {
        "status"    : "diseased",
        "severity"  : "Critical",
        "treatment" : "Immediate fungicide application (metalaxyl). Remove infected plants.",
        "prevention": "Use certified disease-free seeds, ensure drainage.",
    },
    "Powdery Mildew": {
        "status"    : "diseased",
        "severity"  : "Moderate",
        "treatment" : "Apply sulfur-based fungicide or neem oil.",
        "prevention": "Ensure good air circulation, avoid overcrowding.",
    },
    "Bacterial Spot": {
        "status"    : "diseased",
        "severity"  : "High",
        "treatment" : "Copper-based bactericide application.",
        "prevention": "Use disease-free seeds, avoid working when wet.",
    },
    "Leaf Blight": {
        "status"    : "diseased",
        "severity"  : "High",
        "treatment" : "Remove infected leaves, apply appropriate fungicide.",
        "prevention": "Ensure proper spacing and air circulation.",
    },
    "Default": {
        "status"    : "diseased",
        "severity"  : "Moderate",
        "treatment" : "Consult local agricultural extension for specific treatment.",
        "prevention": "Maintain good plant hygiene and monitor regularly.",
    },
}
