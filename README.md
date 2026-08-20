# 🌿 PlantScan AI — Plant Health Prediction System
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=flat&logo=keras&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)

> **IBM SkillsBuild — Data  Science Intern Project (CSRBOX) | Jun 2024 – Aug 2024**

An end-to-end plant disease detection web application powered by **MobileNetV2 Transfer Learning CNN** and **OpenCV** image preprocessing. Upload any leaf image and get an instant diagnosis with **89% accuracy** across 15 disease classes in 3 plant species.

---

## 🖥️ Live Demo

```
python main.py
Open → http://localhost:5000
```

Upload a leaf photo → Get instant disease diagnosis with treatment recommendations!

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/plant-health-prediction.git
cd plant-health-prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Train the model
python model/train.py --data "path/to/PlantVillage" --epochs 10 --batch 64

# 4. Run the web app
python main.py

# 5. Open browser
http://localhost:5000
```

---

## 📁 Project Structure

```
plant_health_system/
│
├── main.py                        ← Flask entry point
├── requirements.txt
├── README.md
├── .gitignore
│
├── app/
│   ├── __init__.py                ← App factory
│   ├── config.py                  ← Settings & 15 class labels
│   ├── model/
│   │   ├── predictor.py           ← CNN inference engine
│   │   └── preprocessor.py        ← OpenCV preprocessing pipeline
│   └── routes/
│       └── api.py                 ← Flask REST API routes
│
├── model/
│   └── train.py                   ← MobileNetV2 training script
│
├── static/
│   ├── css/style.css              ← Dark professional UI
│   └── js/app.js                  ← Drag & drop frontend logic
│
└── templates/
    └── index.html                 ← Single page web application
```

---

## 🧠 Model Architecture

```
Input Leaf Image (any size)
          │
          ▼
   OpenCV Preprocessing
   • Resize → 224×224
   • Gaussian denoising
   • BGR → RGB conversion
   • Normalise [0, 1]
          │
          ▼
   MobileNetV2 Base
   (ImageNet weights — frozen)
          │
          ▼
   GlobalAveragePooling2D
          │
          ▼
   Dense(256, ReLU) → Dropout(0.4)
          │
          ▼
   Dense(128, ReLU) → Dropout(0.3)
          │
          ▼
   Dense(15, Softmax)
          │
          ▼
   Predicted Disease + Confidence
```

---

## 🌱 Supported Plants & Diseases (15 Classes)

| Plant | Disease Classes |
|-------|----------------|
| 🫑 **Pepper** | Bacterial Spot · Healthy |
| 🥔 **Potato** | Early Blight · Late Blight · Healthy |
| 🍅 **Tomato** | Bacterial Spot · Early Blight · Late Blight · Leaf Mold · Septoria Leaf Spot · Spider Mites · Target Spot · Yellow Leaf Curl Virus · Mosaic Virus · Healthy |

---

## 📊 OpenCV Feature Extraction

For every uploaded image the system extracts 6 visual features:

| Feature | Method | Insight |
|---------|--------|---------|
| Green Coverage (%) | HSV masking | Healthy leaf area |
| Lesion Coverage (%) | Brown HSV range | Disease spot area |
| Brightness | Mean pixel intensity | Image quality |
| Contrast | Std dev of grayscale | Texture variation |
| Texture Score | Laplacian variance | Lesion texture |
| Edge Density (%) | Canny edge detection | Leaf structure |

---

## 🎯 Model Performance

| Metric | Value |
|--------|-------|
| Validation Accuracy | **89.18%** |
| Training Epochs | 10 (Phase 1) + 5 (Phase 2) |
| Architecture | MobileNetV2 Transfer Learning |
| Dataset | PlantVillage (16,500+ images) |
| Classes | 15 disease classes |
| Input Size | 224 × 224 px |

---

## 🏋️ Training

```bash
# Download PlantVillage dataset from Kaggle
# https://www.kaggle.com/datasets/emmarex/plantdisease

python model/train.py \
  --data "path/to/PlantVillage" \
  --epochs 10 \
  --batch 64 \
  --out model/plant_model.h5
```

**Two-phase training:**
- **Phase 1** — Train top layers only (MobileNetV2 base frozen)
- **Phase 2** — Fine-tune top 50 base layers with lower learning rate

**Data augmentation applied:**
- Rotation · Width/Height shift · Shear · Zoom
- Horizontal flip · Brightness variation

---

## 📦 Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| `flask` | ≥ 3.0.0 | Web framework & REST API |
| `tensorflow` | ≥ 2.15.0 | MobileNetV2 CNN model |
| `opencv-python` | ≥ 4.9.0 | Image preprocessing & feature extraction |
| `numpy` | ≥ 1.26.0 | Numerical computation |
| `Pillow` | ≥ 10.0.0 | Image utilities |

---

## 💡 Skills Demonstrated

| Skill | Implementation |
|-------|---------------|
| **Deep Learning** | MobileNetV2 Transfer Learning, 2-phase fine-tuning |
| **Computer Vision** | OpenCV preprocessing, HSV masking, Canny edges, Laplacian |
| **Web Development** | Flask REST API, drag-and-drop UI, real-time prediction |
| **Data Augmentation** | Rotation, zoom, flip, brightness — ImageDataGenerator |
| **ML Engineering** | ModelCheckpoint, EarlyStopping, ReduceLROnPlateau |
| **Image Processing** | Denoising, normalisation, feature extraction pipeline |

---

## 🗂️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web application |
| `/predict` | POST | Upload image → get prediction |
| `/health` | GET | Server health check |

---

## 👤 Author

**Smit Velani**
Data Analytics Intern — IBM SkillsBuild (CSRBOX) | Jun 2024 – Aug 2024

---

*Built with Python · Flask · TensorFlow · Keras · OpenCV · MobileNetV2 · PlantVillage Dataset*
