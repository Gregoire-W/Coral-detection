import cv2
import shutil
import os
from tqdm import tqdm


def main(
    ocr_builder,
    video_builder,
    detector_builder,
    utils,
    start,
    end,
    debug,
):
    if debug:
        if os.path.exists("./TEMP/debug"):
            shutil.rmtree("./TEMP/debug")
        os.mkdir("./TEMP/debug")
    if start is None:
        start = 834
    video = video_builder("ocr/video.MP4", start)
    if end is None:
        end = video.frame_count

    ocr = ocr_builder()
    tape_detector = detector_builder()

    detected_list = []

    last_digit = None
    last_digit_frame = None
    last_confidence = None
    img = video.next_frame()
    for frame_number in tqdm(range(video.current_frame, end+1)):
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
                video.save_img(crop_img, f"TEMP/debug/{video.current_frame}_crop.jpg")

            detection = ocr.detect_element(crop_img, utils["map_digits"], video.current_frame, debug=debug)

            if detection:
                # If digit detected is m, add one more check
                correct_m = utils["check_m"](detection[1]) if detection[0] == "m" else True
                if len(detected_list) > 0:
                    last_digit = detected_list[-1][0]
                    last_digit_frame = detected_list[-1][1]
                    last_confidence = detected_list[-1][2]
                digit_backup = None if len(detected_list) < 2 else detected_list[-2][0]
                if correct_m:
                    # If first digit, accept it
                    if not detected_list:
                        detected_list.append((detection[0], video.current_frame, detection[1][-1]))
                        video.save_imgs([crop_img, crop_img], [f"./output/{video.current_frame}.jpg", f"./output/{video.current_frame}_crop.jpg"])
                    # Get the best confidence of the current digit
                    elif detection[0] == last_digit and detection[1][-1] > last_confidence:
                        detected_list.pop()
                        detected_list.append((detection[0], video.current_frame, detection[1][-1]))
                        video.save_imgs([crop_img, crop_img], [f"./output/{video.current_frame}.jpg", f"./output/{video.current_frame}_crop.jpg"])
                    # If we found the next digit, accept it
                    elif last_digit and utils["last_digit"](detection[0]) == last_digit:
                        detected_list.append((detection[0], video.current_frame, detection[1][-1]))
                        video.save_imgs([crop_img, crop_img], [f"./output/{video.current_frame}.jpg", f"./output/{video.current_frame}_crop.jpg"])
                    # If you think last digit wasnt good and you have better confidence here, replace it
                    elif digit_backup and utils["last_digit"](detection[0]) == digit_backup:
                        if detection[1][-1] > last_confidence:
                            detected_list.pop()
                            detected_list.append((detection[0], video.current_frame, detection[1][-1]))
                            video.save_imgs([crop_img, crop_img], [f"./output/{video.current_frame}.jpg", f"./output/{video.current_frame}_crop.jpg"])
                    # If we detect again the backup_digit with a better confidence than last digit, lets assume last digit is a mistake:
                    elif digit_backup == detection[0] and detection[1][-1] > last_confidence:
                        detected_list.pop()  # Delete the wrong digit
                        detected_list.pop()  # Delete the backup digit to replace it with the new one
                        detected_list.append((detection[0], video.current_frame, detection[1][-1]))
                        video.save_imgs([crop_img, crop_img], [f"./output/{video.current_frame}.jpg", f"./output/{video.current_frame}_crop.jpg"])
                    elif detection[0] != last_digit and utils["check_nb_frame"](detection[0], last_digit, video.current_frame, last_digit_frame):
                        detected_list.append((detection[0], video.current_frame, detection[1][-1]))
                        video.save_imgs([crop_img, crop_img], [f"./output/{video.current_frame}.jpg", f"./output/{video.current_frame}_crop.jpg"])

                            #last_digit_frame = video.current_frame
                # Check if you find next odd digit of the backup one
                detection_backup = ocr.detect_element(crop_img, utils["map_backup"], video.current_frame)
                if detection_backup and detection_backup[1][-1] > last_confidence:
                    check = utils["backup_check"](detection_backup, digit_backup)
                    if check:
                        detected_list.pop()

        img = video.next_frame()
        if img is None:
            break
    print([(elem[0], elem[1]) for elem in detected_list])

    video.reset()
    last = 0
    last_digit = None
    final_frames_path = os.listdir("./output")
    for frame_path in final_frames_path:
        frame = os.path.basename(frame_path).split(".")[0]
        if frame not in [elem[1] for elem in detected_list]:
            os.remove(frame_path)
            os.remove(f"{frame}_crop.jpg")
    for (digit, frame, conf) in detected_list:
        print(frame - last)
        for i in range(frame - last):
            video.next_frame()
        video.save_img(video.next_frame(), f"./output/{video.current_frame}.jpg")
        last = video.current_frame

    video.exit()
