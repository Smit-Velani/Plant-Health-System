"""
model/train.py — Train MobileNetV2 on PlantVillage Dataset
"""

import os
import argparse
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── Args ───────────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("--data",   default="data/PlantVillage")
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--batch",  type=int, default=64)
parser.add_argument("--out",    default="model/plant_model.h5")
args = parser.parse_args()

IMG_SIZE = (224, 224)

# ── Data augmentation ──────────────────────────────────────────────────────────
train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=False,
    brightness_range=[0.8, 1.2],
    fill_mode="nearest",
    validation_split=0.2
)

train_data = train_gen.flow_from_directory(
    args.data, target_size=IMG_SIZE,
    batch_size=args.batch, class_mode="categorical",
    subset="training", shuffle=True
)
val_data = train_gen.flow_from_directory(
    args.data, target_size=IMG_SIZE,
    batch_size=args.batch, class_mode="categorical",
    subset="validation", shuffle=False
)

# ✅ Auto-detect AFTER train_data is created
NUM_CLASS = len(train_data.class_indices)
print(f"✅ Auto-detected {NUM_CLASS} classes")

# ── Model ──────────────────────────────────────────────────────────────────────
base = tf.keras.applications.MobileNetV2(
    input_shape=(*IMG_SIZE, 3), include_top=False, weights="imagenet"
)
base.trainable = False

model = tf.keras.Sequential([
    base,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(256, activation="relu"),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(NUM_CLASS, activation="softmax"),
], name="PlantDiseaseNet_MobileNetV2")

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
model.summary()

# ── Callbacks ──────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(args.out), exist_ok=True)
callbacks = [
    ModelCheckpoint(args.out, save_best_only=True, monitor="val_accuracy", verbose=1),
    EarlyStopping(patience=5, restore_best_weights=True, monitor="val_accuracy"),
    ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, verbose=1),
]

# ── Phase 1: Train top layers ──────────────────────────────────────────────────
print("\n📦  Phase 1: Training top layers (base frozen) …")
history1 = model.fit(train_data, epochs=args.epochs,
                     validation_data=val_data, callbacks=callbacks)

# ── Phase 2: Fine-tune top 50 layers ──────────────────────────────────────────
print("\n🔧  Phase 2: Fine-tuning top 50 base layers …")
base.trainable = True
for layer in base.layers[:-50]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
history2 = model.fit(train_data, epochs=5,
                     validation_data=val_data, callbacks=callbacks)

model.save(args.out)
print(f"\n✅  Model saved → {args.out}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.plot(history1.history["accuracy"],     label="Train Acc")
ax1.plot(history1.history["val_accuracy"], label="Val Acc")
ax1.set_title("Accuracy"); ax1.legend()
ax2.plot(history1.history["loss"],         label="Train Loss")
ax2.plot(history1.history["val_loss"],     label="Val Loss")
ax2.set_title("Loss"); ax2.legend()
fig.savefig("model/training_curves.png", dpi=120, bbox_inches="tight")
print("📊  Training curves saved → model/training_curves.png")