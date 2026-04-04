"""
main.py — PlantScan AI — Plant Health Prediction System
IBM SkillsBuild — Data Analytics Intern Project (CSRBOX)
Smit Velan | MS Data Science, Northeastern University
"""

import os
import sys
from app import create_app
from app.config import HOST, PORT, DEBUG

app = create_app()

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🌿  PlantScan AI — Plant Health Prediction           ║
║                                                              ║
║   Deep Learning Plant Disease Detection System               ║
║   MobileNetV2 Transfer Learning + OpenCV Preprocessing       ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   Model     :  MobileNetV2 (Transfer Learning)              ║
║   Classes   :  15 Disease Classes                           ║
║   Plants    :  Pepper · Potato · Tomato                     ║
║   Accuracy  :  ~89% Validation Accuracy                     ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   ▶   Server  :  http://localhost:5000                      ║
║   ▶   Status  :  Starting ...                               ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   IBM SkillsBuild — Data Analytics Intern (CSRBOX)          ║
║   Smit Velan | MS Data Science, Northeastern University      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

if __name__ == "__main__":
    print_banner()
    app.run(host=HOST, port=PORT, debug=DEBUG)