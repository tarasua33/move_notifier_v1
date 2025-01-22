from body_detectors.haar_body_detector import Detector
from video_reader import VideoReader
from read_detect_controller import ReadDetectController
from reporter import Reporter
from move_detector import MoveMedianDetector
from multiprocessing import Queue, Event
from logging import warning
from time import time


BASE_FPS = 20
BOT_ID = "ID"
HAAR_PATH = "cascades"


class App:
    def __init__(self, camera_path: str or int = 0):
        warning("App / INIT start")
        frame_queue = Queue(maxsize=1)
        detected_queue = Queue(maxsize=1)
        stop_event = Event()
        stop_detect_event = Event()

        reader = VideoReader(stop_event, camera_path)
        object_detector = Detector(HAAR_PATH, frame_queue, detected_queue, stop_detect_event)
        reporter = Reporter(BOT_ID)
        move_detector = MoveMedianDetector(BASE_FPS)

        self._controller = ReadDetectController(reader,
                                                object_detector,
                                                move_detector,
                                                detected_queue,
                                                frame_queue,
                                                stop_event,
                                                stop_detect_event,
                                                reporter)
        warning("App / INITED")

    def run(self):
        warning("App / run / start")
        start = time()
        self._controller.run()
        warning(f"App / run / ended/ working time :{time() - start}")

    def stop(self):
        warning("App / stop / call")
        self._controller.stop()
