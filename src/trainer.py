
from ultralytics import YOLO
import os


# Paths
ROOT = os.path.dirname(os.path.dirname(__file__)) if __name__ == '__main__' else '..'
DATA_YAML = os.path.join(ROOT, 'dataset', 'data.yaml')
OUTPUT_DIR = os.path.join(ROOT, 'models')


os.makedirs(OUTPUT_DIR, exist_ok=True)


def train(model='yolov8n.pt', epochs=100, imgsz=640, batch=16):

    y = YOLO(model) # load pretrained
    # Using the .train method
    y.train(data=DATA_YAML, epochs=epochs, imgsz=imgsz, batch=batch, project=OUTPUT_DIR, name='yolov8_coconut', exist_ok=True)


if __name__ == '__main__':
    # Example defaults; adjust for your machine
    train(model='yolov8n.pt', epochs=80, imgsz=640, batch=8)