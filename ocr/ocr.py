import easyocr
import cv2
import numpy as np


class Ocr:

    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def detect_element(self, img, map_digits, frame, threshold=0.15, debug=False):
        img = self.rotate(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if debug:
            cv2.imwrite(f"TEMP/debug/{frame}_rotate.jpg", img)
        results = self.reader.readtext(gray)
        # results = [res for res in results if res[2] > threshold]
        texts = [result[1] for result in results]
        detected = []
        for digit, accepted_values in map_digits.items():
            for i, text in enumerate(texts):
                if any([elem in text for elem in accepted_values]):
                    detected.append((digit, results[i]))
                    break
        if detected:
            detected = max(detected, key=lambda x: x[1][2])
        else:
            detected = None
        return detected

    def rotate(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Canny Edge Detection
        edges = cv2.Canny(gray, 50, 150)

        # Detect lines using Hough Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
        max_angle = 0
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * (180 / np.pi)
                max_angle = max(angle, max_angle)
        # Get image center
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, max_angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result
