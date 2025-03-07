import cv2


class Video:

    def __init__(self, path, start=0):
        self.video = cv2.VideoCapture(path)
        if not self.video.isOpened():
            raise ValueError(f"Error opening the video: {path}")
        self.frame_count = self.video.get(7)
        self.start_from(start)  # Can be automatized
        self.current_frame = start - 1
        self.fps = self.video.get(5)

    def next_frame(self):
        self.current_frame += 1
        ret, frame = self.video.read()
        if ret:
            return frame
        else:
            return None

    def exit(self):
        self.video.release()

    def save_img(self, img, path):
        cv2.imwrite(path, img)

    def start_from(self, img_number):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, img_number)

    def rotate_img(self, img, rotation):
        rotated_img = cv2.rotate(img, rotation)
        return rotated_img
