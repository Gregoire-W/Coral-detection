import easyocr


class Ocr:

    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def detect_element(self, img, map_digits, threshold=0.3):
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
