from ocr.process import main
from ocr.ocr import Ocr
from ocr.video import Video
from tape_detection.tape_detector import TapeDetector
from ocr.utils import get_lower_prediction, MAP_DIGIT, check_m, check_nb_frame
import sys

if __name__ == "__main__":

    start_idx = [i for i in range(len(sys.argv)) if sys.argv[i] == "-start"]
    start = int(sys.argv[start_idx[0]+1]) if start_idx else None

    end_idx = [i for i in range(len(sys.argv)) if sys.argv[i] == "-end"]
    end = int(sys.argv[end_idx[0]+1]) if end_idx else None

    debug_idx = [i for i in range(len(sys.argv)) if sys.argv[i] == "-debug"]
    debug = True if debug_idx else False

    main(
        ocr_builder=Ocr,
        video_builder=Video,
        detector_builder=TapeDetector,
        utils={
            "get_lower_prediction": get_lower_prediction,
            "map_digits": MAP_DIGIT,
            "check_m": check_m,
            "check_nb_frame": check_nb_frame,
        },
        start=start,
        end=end,
        debug=debug,
    )
