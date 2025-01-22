from queue import Queue
from multiprocessing import Event, Process
from cv2 import CascadeClassifier, cvtColor, COLOR_BGR2GRAY, equalizeHist
from time import time
from logging import info


scale_factor_full = 1.1
min_neighbors_full = 5
scale_factor_up = 1.1
min_neighbors_up = 6


class Detector(Process):
    def __init__(self, path: str, frame_queue: Queue, detected_queue: Queue, stop_event: Event):
        super().__init__()

        self.__path = path
        self.__frame_queue = frame_queue
        self.__detected_queue = detected_queue
        self.__stop_event = stop_event

        self.__CATCH_FULL_GRAY = 0
        self.__CATCH_UPPER_GRAY = 0
        self.__CATCH_FULL_EQ_HIST = 0
        self.__CATCH_UPPER_EQ_HIST = 0

        info("Body Detector/ init/ created")

    def run(self):
        info("Body Detector/ run/ start creating classifiers")
        start = time()
        full_body_detector = CascadeClassifier(self.__path + "/haarcascade_fullbody.xml")
        upper_body_detector = CascadeClassifier(self.__path + "/haarcascade_upperbody.xml")
        info(f"Body Detector/ run/ created classifiers/ time {time() - start}")

        frame_queue = self.__frame_queue
        detected_queue = self.__detected_queue

        try:
            info("Body Detector/ run/ main loop start")
            while not self.__stop_event.is_set():
                if not frame_queue.empty():
                    frame = frame_queue.get()

                    start = time()
                    bodies, frame_to_save = self._detect(frame, full_body_detector, upper_body_detector)
                    print(f'duration: {time() - start}')

                    if not detected_queue.full() and bodies is not None and len(bodies) > 0:
                        detected_queue.put({"frame": frame_to_save, "result": bodies})
        finally:

            print(f"__CATCH_FULL_GRAY: {self.__CATCH_FULL_GRAY}")
            print(f"__CATCH_UPPER_GRAY: {self.__CATCH_UPPER_GRAY}")
            print(f"__CATCH_FULL_EQ_HIST: {self.__CATCH_FULL_EQ_HIST}")
            print(f"__CATCH_UPPER_EQ_HIST: {self.__CATCH_UPPER_EQ_HIST}")

            info(f"Body Detector/ run/ finally /"
                 f"{self.__CATCH_FULL_GRAY} /"
                 f"{self.__CATCH_UPPER_GRAY} /"
                 f"{self.__CATCH_FULL_EQ_HIST}/"
                 f"{self.__CATCH_UPPER_EQ_HIST}")

            if not frame_queue.empty():
                info("Body Detector/ run/ finally / cleaning frame_queue")
                frame_queue.get()
                info("Body Detector/ run/ finally / CLEANED frame_queue")

    def _detect(self, frame, full_body_detector: CascadeClassifier, upper_body_detector: CascadeClassifier):
        frame_to_save = frame

        gray = cvtColor(frame, COLOR_BGR2GRAY)
        bodies = full_body_detector.detectMultiScale(gray, scale_factor_full, min_neighbors_full)
        # bodies = full_body_detector.detectMultiScale(gray)

        # DEBUG
        if bodies is not None and len(bodies) > 0:
            frame_to_save = gray
            self.__CATCH_FULL_GRAY += 1
        # //////

        if bodies is None or len(bodies) == 0:
            bodies = upper_body_detector.detectMultiScale(gray, scale_factor_up, min_neighbors_up)
            # DEBUG
            if bodies is not None and len(bodies) > 0:
                frame_to_save = gray
                self.__CATCH_UPPER_GRAY += 1
            # ///////

        if bodies is None or len(bodies) == 0:
            eq_hist = equalizeHist(gray)

            bodies = full_body_detector.detectMultiScale(eq_hist, scale_factor_full, min_neighbors_full)
            # DEBUG
            if bodies is not None and len(bodies) > 0:
                frame_to_save = eq_hist
                self.__CATCH_FULL_EQ_HIST += 1
            # //////

            if bodies is None or len(bodies) == 0:
                bodies = upper_body_detector.detectMultiScale(eq_hist, scale_factor_up, min_neighbors_up)
                # DEBUG
                if bodies is not None and len(bodies) > 0:
                    frame_to_save = eq_hist
                    self.__CATCH_UPPER_EQ_HIST += 1
                # /////////

        return bodies, frame_to_save