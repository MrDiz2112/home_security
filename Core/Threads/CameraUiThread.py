import logging

import cv2
import numpy as np
from typing import Callable, List, Tuple

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

from Core import CameraManager


class CameraUiThread(QThread):
    on_new_image = pyqtSignal(QImage)

    def __init__(self, manager: CameraManager):
        super().__init__()

        self.__manager: CameraManager = manager

        self.__is_running = False
        self.__get_frame: Callable[[], np.ndarray] = None

        self.__motions_roi_to_draw = []
        self.__faces_roi_to_draw = []

        self.__color_motion = (0, 0, 255)
        self.__color_face = (0, 255, 182)
        self.__thickness = 2

        self.__manager.on_motion_roi_changed.connect(self.__update_motion_roi)
        self.__manager.on_faces_roi_changed.connect(self.__update_faces_roi)

    def run(self):
        self.__is_running = True

        self.__ui_thread_info("Start Camera UI thread")

        while self.__is_running:
            #TODO: тащить из менеджера roi для прорисовки
            frame = self.__manager.get_camera_image()

            self.__draw_rect(frame, self.__motions_roi_to_draw, self.__color_motion)
            self.__draw_rect(frame, self.__faces_roi_to_draw, self.__color_face)

            image = self.__get_qimage(frame)

            self.on_new_image.emit(image)

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

    def __draw_rect(self, img: np.ndarray, roi: List[Tuple[int, int, int, int]], color: Tuple[int, int, int]):
        if len(roi) != 0:
            for motion_roi in roi:
                try:
                    x,y,w,h = motion_roi
                    if  x >= 0 and y >= 0 and w >= 0 and h >= 0:
                        cv2.rectangle(img, (x,y), (x+w, y+h), color, self.__thickness)
                except Exception as ex:
                    self.__manager_error(f"Failed to draw rect. {ex}")

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
