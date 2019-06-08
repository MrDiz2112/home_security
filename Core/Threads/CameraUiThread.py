import logging
import threading
import time
from threading import Thread

import cv2
import numpy as np
from typing import Callable, List, Tuple

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

from Core import CameraManager
from Core.Data import RoiData


class CameraUiThread(QThread):
    on_new_image = pyqtSignal(QImage)

    def __init__(self, fps: float):
        super().__init__()

        self.__is_running = False

        self.__motions_roi_to_draw = []
        self.__faces_roi_to_draw = []

        self.__color_motion = (0, 0, 255)
        self.__color_face = (0, 255, 182)
        self.__thickness = 2

        self.__frame_wait = 1 / fps

        self.__get_actual_data: Callable[[], Tuple[np.ndarray, List[RoiData]]] = None

    def run(self):
        try:
            threading.current_thread().name = "UiThread"
            self.__is_running = True

            self.__ui_thread_info("Start Camera UI thread")

            if self.__get_actual_data is None:
                self.__ui_thread_warn("Caller is not assigned")
                return

            while self.__is_running:
                start_time = time.time()

                frame, roi_list = self.__get_actual_data()

                if frame is None:
                    continue

                for i in range(len(roi_list)):
                    roi = roi_list.pop()
                    self.__draw_rect(frame, roi)

                image = self.__get_qimage(frame)

                self.on_new_image.emit(image)

                end_time = time.time()

                if end_time - start_time < self.__frame_wait:
                    time.sleep(self.__frame_wait - (end_time - start_time))
        except Exception as ex:
            self.__ui_thread_error(f"{ex}")

    def stop(self):
        self.__is_running = False

    def __get_qimage(self, image: np.ndarray) -> QImage:
        """
        Преобразует изображение из формата numpy в QImage
        """
        height, width, colors = image.shape
        bytesPerLine = 3 * width

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def __draw_rect(self, img: np.ndarray, roi: RoiData):
        if len(roi.roi) != 0:
            try:
                if  roi.is_motion:
                    color = self.__color_motion
                else:
                    color = self.__color_face

                x,y,w,h = roi.roi
                if  x >= 0 and y >= 0 and w >= 0 and h >= 0:
                    cv2.rectangle(img, (x,y), (x+w, y+h), color, self.__thickness)
            except Exception as ex:
                self.__ui_thread_error(f"Failed to draw rect. {ex}")

    def assign_caller(self, callable_name: callable):
        self.__get_actual_data = callable_name

    def __update_motion_roi(self):
        self.__motions_roi_to_draw = self.__manager.get_motions_roi_to_draw()[:]
        self.__manager.clear_motions_roi_to_draw()

    def __update_faces_roi(self):
        self.__faces_roi_to_draw = self.__manager.get_faces_roi_to_draw()[:]
        self.__manager.clear_faces_roi_to_draw()

    def __ui_thread_info(self, msg:str):
        message = f"[UI Thread] {msg}"
        logging.info(message)

    def __ui_thread_warn(self, msg:str):
        message = f"[UI Thread] {msg}"
        logging.warning(message)

    def __ui_thread_error(self, msg:str):
        message = f"[UI Thread] {msg}"
        logging.error(message)
