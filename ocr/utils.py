MAP_DIGIT = {
    "20": ["20"],
    "40": ["40"],
    "60": ["60"],
    "80": ["80", "B T", "B0", "BO"],
    "m": ["m", "M"],
}

MAP_BACKUP = {
    "10": ["10"],
    "30": ["30"],
    "50": ["50"],
    "70": ["70"],
    "90": ["90"],
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
    print(f"m_height: {m_height}")
    return m_height >= 40


def check_nb_frame(digit, last_digit, last_digit_frame, current_frame):
    if last_digit_frame is None:
        return True, True
    digit_list = list(MAP_DIGIT.keys())
    digit_idx = [i for i in range(len(digit_list)) if digit_list[i] == digit][0]
    last_digit_idx = [i for i in range(len(digit_list)) if digit_list[i] == last_digit][0]
    if digit_idx > last_digit_idx:
        min_diff = digit_idx - last_digit_idx
    else:
        min_diff = 5 - last_digit_idx + digit_idx

    actual_diff = current_frame - last_digit_frame
    return (min_diff * 23 <= actual_diff) or (min_diff==1 and min_diff * 14 <= actual_diff), min_diff == 1


def backup_check(detection, digit_backup):
    if detection and digit_backup:
        return detection[0] == next_digit(digit_backup, 10)
    else:
        return False


def next_digit(digit, rate=20):
    if digit == "m":
        return str(rate)
    elif int(digit) + rate > 100:
        return str(int(digit) + rate - 100)
    else:
        return str(int(digit) + rate)


def last_digit(digit, rate=20):
    if digit == "m":
        return str(100 - rate)
    elif int(digit) - rate < 0:
        return str(int(digit) - rate + 100)
    else:
        return str(int(digit) - rate)
