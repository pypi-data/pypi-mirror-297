import cv2
from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path):
        print("Loading YOLO model...")
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame)
        bboxes = []
        for result in results:
            bboxes.append(result.boxes)
        return bboxes


