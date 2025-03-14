from ultralytics import YOLO


class TapeDetector():

    def __init__(self):
        self.model = YOLO("tape_detection/best.pt")

    def predict(self, img, save=False):
        predictions = self.model(img, save=save, verbose=False)
        return predictions
