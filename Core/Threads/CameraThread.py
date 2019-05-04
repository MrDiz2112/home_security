import time

import cv2
import logging
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

from Core import Manager


class CameraThread(QThread):
    def __init__(self, cam_port: int, fps: float, manager: Manager):
        super().__init__()

        self.__cam = None
        self.__manager: Manager = manager
        self.__is_running: bool = False
        self.__cam_port: int = cam_port
        self.__frame_wait = 1/ fps

    def run(self):
        if self.__manager is None:
            self.__cam_thread_warn("Manager is null!")
            return

        self.__is_running = True
        self.__cam_thread_info(f"Camera {self.__cam_port} is running")

        if not self.__open():
            raise Exception(f"Failed to open camera {self.__cam_port}")

        self.__cam_thread_info(f"Start frame grabber")

        while self.__is_running:
            start_time = time.time()

            res, frame = self.__cam.read()

            if res:
                self.__manager.put_camera_frame(frame)

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

                self.sleep(5)

    def __open(self):
        cam = None

        try:
            cam = cv2.VideoCapture(self.__cam_port)
        except Exception as ex:
            self.__cam_thread_error(f"Failed to open camera {self.__cam_port}. {ex}")
            return False
        finally:
            self.__cam = cam

        if not cam.isOpened():
            self.__cam_thread_warn(f"Camera {self.__cam_port} isn't open")
            return False

        res, img = cam.read()
        if not res:
            self.__cam_thread_warn("Invalid frame on init")
            return False

        self.__cam_thread_info(f"Camera {self.__cam_port} opened")

        return True

    def stop(self):
        self.__is_running = False

        self.__cam_thread_info(f"Camera {self.__cam_port} stopped")
        if self.__cam is not None:
            self.__cam.release()

        self.__cam_thread_info(f"Camera {self.__cam_port} released")

    def __release(self):
        self.__cam_thread_info(f"Releasing camera {self.__cam_port}")
        self.stop()

    def __str__(self):
        return f"Camera {self.__cam_port}"

    def __cam_thread_info(self, msg:str):
        message = f"[Camera {self.__cam_port} Thread] {msg}"
        logging.info(message)

    def __cam_thread_warn(self, msg:str):
        message = f"[Camera {self.__cam_port} Thread] {msg}"
        logging.warning(message)

    def __cam_thread_error(self, msg:str):
        message = f"[Camera {self.__cam_port} Thread] {msg}"
        logging.error(message)
