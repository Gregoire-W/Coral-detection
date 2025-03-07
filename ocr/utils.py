MAP_DIGIT = {
    "20": ["20"],
    "40": ["40"],
    "60": ["60"],
    "80": ["80"],
    "m": ["m"],
}


def get_lower_prediction(predictions):
    max_y = 0
    bbox = None
    for prediction in predictions:
        for box in prediction.boxes:
            (x, y, w, h) = [round(float(elem)) for elem in box.xywh[0]]
            if y + h//2 > max_y:
                max_y = y + h//2
                bbox = (x, y, w, h)
    return bbox


def check_m(result):
    coordinates, text, conf = result
    p1, p2, p3, p4 = coordinates
    m_height = (p4[1]-p1[1] + p3[1]-p2[1]) // 2
    if m_height >= 45:
        print(m_height)
    return m_height >= 45
