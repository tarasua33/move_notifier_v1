from video_reader import VideoReader
from body_detectors.haar_body_detector import Detector
from reporter import Reporter
from cv2 import imshow, waitKey, destroyAllWindows, rectangle
import time
from move_detector import MoveMedianDetector
from logging import info


TIME_BTW_SENDING = 10     # seconds


class ReadDetectController:
    def __init__(self,
                 video_reader: VideoReader,
                 object_detector: Detector,
                 move_detector: MoveMedianDetector,
                 detected_queue,
                 frame_queue,
                 stop_event,
                 stop_detect_event,
                 reporter: Reporter):
        self.__video_reader = video_reader
        self.__object_detector = object_detector
        self.__move_detector = move_detector
        self.__detected_queue = detected_queue
        self.__frame_queue = frame_queue
        self.__stop_event = stop_event
        self.__stop_detect_event = stop_detect_event
        self.__reporter = reporter
        self.__last_time_sent = time.time()
        info("Controller/ init/ created")

    def run(self):
        self.__video_reader.start()
        self.__object_detector.start()
        show_frame = None
        first_loop = True

        try:
            info("Controller/ run/ Start main loop")
            while not self.__stop_event.is_set():
                if self.__video_reader.frame is not None:
                    frame = self.__video_reader.frame
                    if first_loop:
                        first_loop = False
                        show_frame = frame.copy()

                    self._moving_detect_update(frame)
                    interval_send_ended = (time.time() - self.__last_time_sent) > TIME_BTW_SENDING
                    marks, checked_frame = self._get_detected_objects(interval_send_ended)
                    self._draw_send_marks(marks, checked_frame, interval_send_ended)

                    if checked_frame is not None:
                        show_frame = checked_frame

                    if show_frame is not None:
                        imshow("Video", show_frame)

                    self.__video_reader.frame = None

                if waitKey(1) & 0xFF == ord('q'):
                    info("Controller/ run/ main loop/ Q - pushed")
                    self.__stop_event.set()
                    info("Controller/ run/ MainEvent stop called")
                    break
        finally:
            info("Controller/ run/ Finally main loop")
            self.__stop_event.set()
            info("Controller/ run/ MainEvent stop called")
            self.__video_reader.join()
            info("Controller/ run/ Video Reader joined")
            self.__stop_detect_event.set()
            info("Controller/ run/ DetectorEvent stop call")
            self.__object_detector.join()
            info("Controller/ run/ ObjectDetector joined")
            if not self.__detected_queue.empty():
                info("Controller/ run/ Detector queue cleaning")
                self.__detected_queue.get()
                info("Controller/ run/ Detector queue cleaned")
            destroyAllWindows()
            print("//////////- closed -////////////////")

        print("//////////- End -////////////////")

    def stop(self):
        info("Controller/ stop/ stop calling")
        self.__stop_event.set()
        info("Controller/ stop/ stop called")

    def _moving_detect_update(self, frame):
        move_detector = self.__move_detector
        move_detector.next_update(frame)

        if move_detector.is_change and not self.__frame_queue.full():
            self.__frame_queue.put(frame)

    def _get_detected_objects(self, interval_send_ended: float or int):
        if not self.__detected_queue.empty() \
                and interval_send_ended:
            data = self.__detected_queue.get()
            marks = data["result"]
            checked_frame = data["frame"]
            self.__last_time_sent = time.time()
        else:
            checked_frame = None
            marks = None

        return marks, checked_frame

    def _draw_send_marks(self, marks, checked_frame, interval_send_ended):
        if marks is not None and checked_frame is not None:
            self.draw_haar_marks(marks, checked_frame)
            if interval_send_ended:
                self.__reporter.report(checked_frame)

    @staticmethod
    def draw_haar_marks(objects, frame):
        for (x, y, w, h) in objects:
            rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    # @staticmethod
    # def draw_rec(objects, frame):
        # mp.solutions.drawing_utils.draw_detection(frame, objects)
        # for item in objects:
            # mp.solutions.drawing_utils.draw_detection(frame, item)

