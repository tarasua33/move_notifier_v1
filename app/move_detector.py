from numpy import median, array, uint8
from cv2 import absdiff, threshold, THRESH_BINARY
from logging import info

MAX_FRAMES = 20
THRESHOLD_TO_MOVE = 0.15
MULTIPLIER_FPS = 2


class MoveMedianDetector:
    def __init__(self, fps: int):

        self.is_change = None
        self.diff_frames = None
        self.__median_frame = None
        self.__one_to_frame = fps * MULTIPLIER_FPS
        self.__frames = []
        self.__counter = 0
        info("Move Detector/ init/ created")

    def next_update(self, frame):
        self.is_change = False
        self.__counter += 1

        if self.__counter % self.__one_to_frame == 0:
            if self.__median_frame is not None:
                diff_frame = absdiff(frame, self.__median_frame)

                _, diff_frame = threshold(diff_frame, 30, 255, THRESH_BINARY)

                self.diff_frames = diff_frame

                change_sum = diff_frame.sum()
                percent_changes = change_sum / diff_frame.size
                self.is_change = percent_changes >= THRESHOLD_TO_MOVE

            self.__counter = 0
            if len(self.__frames) >= MAX_FRAMES:
                self.__frames.pop(0)

            self.__frames.append(frame)

            self.__median_frame = median(array(self.__frames), axis=0).astype(uint8)
