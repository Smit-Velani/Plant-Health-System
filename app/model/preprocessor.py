"""
preprocessor.py — Image preprocessing pipeline using OpenCV
"""

import cv2
import numpy as np
from app.config import IMG_SIZE


class ImagePreprocessor:
    """
    Handles all image preprocessing steps before feeding into the CNN model.
    Uses OpenCV for image manipulation and feature analysis.
    """

    def __init__(self, img_size=IMG_SIZE):
        self.img_size = img_size

    # ── Main pipeline ──────────────────────────────────────────────────────────

    def preprocess(self, image_path: str) -> np.ndarray:
        """
        Full preprocessing pipeline:
          Load → Resize → Denoise → Normalise → Expand dims

        Returns numpy array ready for model inference.
        """
        img = self._load(image_path)
        img = self._resize(img)
        img = self._denoise(img)
        img = self._normalise(img)
        img = np.expand_dims(img, axis=0)   # (1, 224, 224, 3)
        return img

    def extract_features(self, image_path: str) -> dict:
        """
        Extract visual features from the leaf image for display purposes.
        Returns a dict with colour histogram stats, texture, brightness etc.
        """
        img_bgr = self._load(image_path)
        img_bgr = self._resize(img_bgr)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        gray    = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        hsv     = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

        # Green coverage (plant health indicator)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        green_mask  = cv2.inRange(hsv, lower_green, upper_green)
        green_pct   = round((np.sum(green_mask > 0) / green_mask.size) * 100, 1)

        # Brown/disease spots
        lower_brown = np.array([10, 40, 40])
        upper_brown = np.array([30, 255, 200])
        brown_mask  = cv2.inRange(hsv, lower_brown, upper_brown)
        brown_pct   = round((np.sum(brown_mask > 0) / brown_mask.size) * 100, 1)

        # Brightness & contrast
        brightness  = round(float(np.mean(gray)), 1)
        contrast    = round(float(np.std(gray)), 1)

        # Texture — Laplacian variance (sharpness / lesion texture)
        laplacian   = cv2.Laplacian(gray, cv2.CV_64F)
        texture     = round(float(laplacian.var()), 1)

        # Edge density (via Canny)
        edges       = cv2.Canny(gray, 50, 150)
        edge_density= round((np.sum(edges > 0) / edges.size) * 100, 1)

        return {
            "green_coverage" : green_pct,
            "lesion_coverage": brown_pct,
            "brightness"     : brightness,
            "contrast"       : contrast,
            "texture_score"  : texture,
            "edge_density"   : edge_density,
            "image_size"     : f"{img_bgr.shape[1]} × {img_bgr.shape[0]} px",
        }

    # ── Private helpers ────────────────────────────────────────────────────────

    def _load(self, path: str) -> np.ndarray:
        img = cv2.imread(path)
        if img is None:
            raise ValueError(f"Could not load image: {path}")
        return img

    def _resize(self, img: np.ndarray) -> np.ndarray:
        return cv2.resize(img, self.img_size, interpolation=cv2.INTER_AREA)

    @staticmethod
    def _denoise(img: np.ndarray) -> np.ndarray:
        return cv2.fastNlMeansDenoisingColored(img, None, 6, 6, 7, 21)

    @staticmethod
    def _normalise(img: np.ndarray) -> np.ndarray:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img_rgb.astype(np.float32) / 255.0
