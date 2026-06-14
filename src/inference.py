# src/inference.py
import os
from ultralytics import YOLO

# Detect project root automatically (E:\coconut\coconut_disease_project)
ROOT = os.path.dirname(os.path.dirname(__file__))

# Path to trained best.pt model
MODEL_PATH = os.path.join(ROOT, "models", "best.pt")

print("MODEL PATH:", MODEL_PATH)

# Safety check
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at: {MODEL_PATH}")

# Load YOLO model
model = YOLO(MODEL_PATH)


def detect_from_image(image_path):
    """
    Runs YOLOv8/v11 detection on a given image and returns the result.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    results = model(image_path)   # performs inference
    return results
