from threading import Thread, Event
from cv2 import VideoCapture, resize, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from logging import info

BASE_W = 480
BASE_H = 320
BASE_FPS = 20


class VideoReader(Thread):
    def __init__(self, stop_event: Event, video_path=0):
        super().__init__()

        self.__live = VideoCapture(video_path)
        info(f"VideoReader / init / live is open {self.__live.isOpened()}")
        self.frame = None
        self.__stop_event = stop_event

        self._set_up_live()

    def _set_up_live(self):
        # DOESN'T WORK FOR FFMPEG
        live = self.__live
        live.set(CAP_PROP_FRAME_WIDTH, BASE_W)
        live.set(CAP_PROP_FRAME_HEIGHT, BASE_H)
        live.set(CAP_PROP_FPS, BASE_FPS)
        info(f"VideoReader / set_up / FPS: {live.get(CAP_PROP_FPS)}")

    def run(self):
        info("VideoReader / run / main loop VideoReader")
        while self.__live.isOpened() and not self.__stop_event.is_set():
            ret, frame = self.__live.read()
            if ret:
                # FOR FFMPEG
                self.frame = resize(frame, (BASE_W, BASE_H)).copy()
                # if not self.__frame_queue.full():
                #     self.__frame_queue.put(frame)

        info("VideoReader / run / main loop exit release")
        self.__live.release()
        info("VideoReader / run / main loop exit released")
