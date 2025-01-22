# from mediapipe import solutions
# from queue import Queue
# from multiprocessing import Event, Process
# from cv2 import resize
#
#
# BASE_W = 480
#
#
# class Detector(Process):
#     def __init__(self, frame_queue: Queue, detected_queue: Queue, stop_event: Event):
#         super().__init__()
#
#         self.__frame_queue = frame_queue
#         self.__detected_queue = detected_queue
#         self.__stop_event = stop_event
#         self.__detector = None
#
#     def run(self):
#         pose_detection = solutions.pose
#         self.__detector = pose_detection.Pose()
#
#         try:
#             while not self.__stop_event.is_set():
#                 if not self.__frame_queue.empty():
#                     frame = resize(self.__frame_queue.get(), (BASE_W, BASE_W))
#                     results = self.__detector.process(frame)
#                     # self.__detector.close()
#
#                     if not self.__detected_queue.full() and results.pose_landmarks is not None:
#                         self.__detected_queue.put({"frame": frame, "result": results.pose_landmarks})
#         finally:
#             self.__detector.close()
#             # time.sleep(0.1)
#             if not self.__frame_queue.empty():
#                 self.__frame_queue.get()
