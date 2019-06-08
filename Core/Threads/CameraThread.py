import threading
import time
from queue import Queue
from threading import Thread

import cv2
import logging
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

from Core import CameraManager


class CameraThread(Thread):
    def __init__(self, name: str, camera_source, fps: float):
        super().__init__()

        self.__name = name
        self.__actual_frame = None

        self.__cam = None
        self.__is_running: bool = False
        self.__camera_source = camera_source
        self.__frame_wait = 1 / fps

    def get_actual_frame(self) -> np.ndarray:
        if self.__actual_frame is None:
            return None

        img = self.__actual_frame[:]
        self.__actual_frame = None
        return img

    def run(self):
        threading.current_thread().name = "CameraThread"

        self.__cam_thread_info(f"Camera {self.__camera_source} is running")

        if not self.__open():
            raise Exception(f"Failed to open camera {self.__camera_source}")

        self.__cam_thread_info(f"Start frame grabber")

        while self.__is_running:
            start_time = time.time()
            res, frame = self.__cam.read()

            if res:
                self.__actual_frame = frame
                end_time = time.time()

                if end_time - start_time < self.__frame_wait:
                    time.sleep(self.__frame_wait - (end_time - start_time))

                continue

            # If failed
            self.__cam_thread_warn("Frame was not null")
            self.__release()

            attempt = 0
            while True:
                self.__cam_thread_info(f"Trying to reopen camera. Attempt {attempt}")
                success = self.__open()
                attempt += 1

                if success:
                    self.__cam_thread_info("Connection restored")
                    break

                time.sleep(5)

    def __open(self):
        cam = None

        try:
            cam = cv2.VideoCapture(self.__camera_source)
        except Exception as ex:
            self.__cam_thread_error(f"Failed to open camera {self.__camera_source}. {ex}")
            return False
        finally:
            self.__cam = cam

        if not cam.isOpened():
            self.__cam_thread_warn(f"Camera {self.__camera_source} isn't open")
            return False

        res, img = cam.read()
        if not res:
            self.__cam_thread_warn("Invalid frame on init")
            return False

        self.__cam_thread_info(f"Camera {self.__camera_source} opened")

        self.__is_running = True

        return True

    def stop(self):
        self.__is_running = False

        self.__cam_thread_info(f"Camera {self.__camera_source} stopped")
        if self.__cam is not None:
            self.__cam.release()

        self.__cam_thread_info(f"Camera {self.__camera_source} released")

    def __release(self):
        self.__cam_thread_info(f"Releasing camera {self.__camera_source}")
        self.stop()

    def __str__(self):
        return f"Camera {self.__camera_source}"

    def __cam_thread_info(self, msg:str):
        message = f"[Camera {self.__name} Thread] {msg}"
        logging.info(message)

    def __cam_thread_warn(self, msg:str):
        message = f"[Camera {self.__name} Thread] {msg}"
        logging.warning(message)

    def __cam_thread_error(self, msg:str):
        message = f"[Camera {self.__name} Thread] {msg}"
        logging.error(message)
