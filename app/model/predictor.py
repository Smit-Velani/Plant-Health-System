"""
predictor.py — CNN Model Predictor using MobileNetV2 Transfer Learning
"""

import os
import numpy as np
import tensorflow as tf
from app.config import MODEL_PATH, CLASSES, CONFIDENCE_THRESHOLD, DISEASE_INFO, IMG_SIZE
from app.model.preprocessor import ImagePreprocessor


class PlantDiseasePredictor:
    """
    Loads the trained MobileNetV2 CNN model and runs inference
    on preprocessed leaf images to predict plant disease.
    """

    def __init__(self):
        self.model        = None
        self.preprocessor = ImagePreprocessor()
        self._load_model()

    # ── Model loading ──────────────────────────────────────────────────────────

    def _load_model(self):
        """Load saved model from disk, or build a fresh one if not found."""
        if os.path.exists(MODEL_PATH):
            print(f"✅  Loading model from {MODEL_PATH}")
            self.model = tf.keras.models.load_model(MODEL_PATH)
        else:
            print("⚠️   No saved model found — building MobileNetV2 base model.")
            print("     Run model/train.py to train on PlantVillage dataset.")
            self.model = self._build_model()

    def _build_model(self):
        """
        Build MobileNetV2 transfer learning model.
        Architecture:
          MobileNetV2 (ImageNet weights, frozen) →
          GlobalAveragePooling2D →
          Dense(256, relu) → Dropout(0.4) →
          Dense(128, relu) → Dropout(0.3) →
          Dense(38, softmax)
        """
        base = tf.keras.applications.MobileNetV2(
            input_shape=(*IMG_SIZE, 3),
            include_top=False,
            weights="imagenet"
        )
        base.trainable = False   # freeze base layers

        model = tf.keras.Sequential([
            base,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dropout(0.4),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(len(CLASSES), activation="softmax"),
        ], name="PlantDiseaseNet_MobileNetV2")

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        return model

    # ── Prediction ─────────────────────────────────────────────────────────────

    def predict(self, image_path: str) -> dict:
        """
        Run full prediction pipeline on a leaf image.

        Returns
        -------
        dict with keys:
          predicted_class, plant, disease, confidence, status,
          severity, treatment, prevention, top5, features
        """
        # Preprocess
        tensor   = self.preprocessor.preprocess(image_path)
        features = self.preprocessor.extract_features(image_path)

        # Inference
        preds    = self.model.predict(tensor, verbose=0)[0]
        top_idx  = int(np.argmax(preds))
        top_conf = float(preds[top_idx])

        # Top-5 predictions
        top5_idx  = np.argsort(preds)[::-1][:5]
        top5      = [
            {"class": CLASSES[i], "confidence": round(float(preds[i]) * 100, 1)}
            for i in top5_idx
        ]

        # Parse class label
        predicted_class = CLASSES[top_idx]
        parts  = predicted_class.split(" — ")
        plant  = parts[0] if len(parts) > 1 else "Unknown"
        disease= parts[1] if len(parts) > 1 else predicted_class

        # Fallback if below threshold
        if top_conf < CONFIDENCE_THRESHOLD:
            return {
                "predicted_class": "Low Confidence",
                "plant"          : "Unknown",
                "disease"        : "Unable to determine",
                "confidence"     : round(top_conf * 100, 1),
                "status"         : "uncertain",
                "severity"       : "Unknown",
                "treatment"      : "Please upload a clearer image of the leaf.",
                "prevention"     : "Ensure good lighting and focus on the leaf.",
                "top5"           : top5,
                "features"       : features,
            }

        # Get disease info
        info_key = disease if disease in DISEASE_INFO else "Default"
        if "Healthy" in disease:
            info_key = "Healthy"
        info = DISEASE_INFO[info_key]

        return {
            "predicted_class": predicted_class,
            "plant"          : plant,
            "disease"        : disease,
            "confidence"     : round(top_conf * 100, 1),
            "status"         : info["status"],
            "severity"       : info["severity"],
            "treatment"      : info["treatment"],
            "prevention"     : info["prevention"],
            "top5"           : top5,
            "features"       : features,
        }
