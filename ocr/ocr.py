import easyocr
import cv2


class Ocr:

    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def detect_element(self, img, map_digits, threshold=0.15):
        # Pre process img for ocr
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #blurred = cv2.medianBlur(gray, 3)
        #_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        results = self.reader.readtext(img)
        print(rf"texts: {[result[1] for result in results]},conf:{[result[2] for result in results]}")
        results = [res for res in results if res[2] > threshold]
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
