import cv2


def main(
    ocr_builder,
    video_builder,
    detector_builder,
    utils,
    start,
    end,
    debug,
):
    if start is None:
        start = 834
    video = video_builder("ocr/video.MP4", start)
    if end is None:
        end = video.frame_count

    ocr = ocr_builder()
    tape_detector = detector_builder()

    detected_list = []

    last_digit = ""
    last_digit_frame = None
    img = video.next_frame()
    while img is not None and video.current_frame <= end:
        predictions = tape_detector.predict(img)
        bbox = utils["get_lower_prediction"](predictions)
        if bbox:
            x, y, w, h = bbox
            mid_h = h//2
            mid_w = w//2
            y_crop = max(y-mid_h, y+mid_h-300)
            crop_img = img[y_crop:y+mid_h, x-mid_w:x+w]
            crop_img = video.rotate_img(crop_img, cv2.ROTATE_90_CLOCKWISE)
            if debug:
                video.save_img(crop_img, f"TEMP/debug/crop_{video.current_frame}.jpg")
                video.save_img(img, f"TEMP/debug/{video.current_frame}.jpg")

            detection = ocr.detect_element(crop_img, utils["map_digits"])
            if detection:
                correct_m = utils["check_m"](detection[1]) if detection[0] == "m" else True
                check_nb_frame = utils["check_nb_frame"](detection[0], last_digit, last_digit_frame, video.current_frame)
                if correct_m and check_nb_frame:
                    last_digit = detection[0]
                    last_digit_frame = video.current_frame
                    detected_list.append((detection[0], video.current_frame))
                    p1 = int(detection[1][0][0][0]), int(detection[1][0][0][1])
                    p2 = int(detection[1][0][2][0]), int(detection[1][0][2][1])
                    crop_img = cv2.rectangle(crop_img, p1, p2, (255, 0, 0), thickness=2)
                    video.save_img(crop_img, "TEMP/current/crop_img.jpg")
                    # input(f"digit: {detection[0]} detected at frame: {video.current_frame}")

        img = video.next_frame()
    print(detected_list)
    video.exit()
