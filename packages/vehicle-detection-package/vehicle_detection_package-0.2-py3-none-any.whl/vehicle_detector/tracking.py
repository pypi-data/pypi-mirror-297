from sort import Sort
import numpy as np

class VehicleTracker:
    def __init__(self):
        print("Initializing SORT tracker...")
        self.tracker = Sort()

    def update(self, detections):
        # Converting detections into appropriate format (if necessary)
        np_detections = np.array(detections)
        tracked_objects = self.tracker.update(np_detections)
        return tracked_objects

