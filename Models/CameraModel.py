import logging
from typing import List

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

from Core import Manager
from Core.Threads import CameraThread
from Models import FaceDetectionModel, MotionDetectionModel


class CameraModel(QtCore.QObject):
    on_thread_finished = pyqtSignal()

    def __init__(self, cascade_filepath: str, camera_port: int, fps: float, manager: Manager):
        super().__init__()

        self.__manager = manager
        self.__camera_port = camera_port
        self.__fps = fps

        self.__camera_thread = CameraThread(self.__camera_port, self.__fps, self.__manager)
        self.__camera_thread.finished.connect(self.__grab_finished)

        self._colorFace = (0, 255, 182)
        self._colorMotion = (0, 0, 255)
        self._thickness = 2

        self._face_detection_model = FaceDetectionModel(cascade_filepath)
        self._motion_detection_model = MotionDetectionModel()

    # Методы для View

    # TODO: обработка флага отображения обработки
    def start_frame_grabber(self, is_display_processing: bool) -> None:
        self.__camera_thread.start(QThread.HighestPriority)

    def stop_frame_grabber(self):
        self.__camera_thread.stop()

    @pyqtSlot()
    def __grab_finished(self):
        self.__camera_model_info("Frame grabber finished")
        self.on_thread_finished.emit()

    # Методы бизнес логики

    def process_image_data(self, image_data: np.ndarray) -> QtGui.QImage:
        """
        Пропускает изображение с камеры через все обработчики и возвращает
        результат
        :param image_data: изображение np.array
        :return: обработанное изображение  QImage
        """
        self.detect_motion(image_data)
        self.detect_faces(image_data)

        image = self.get_qimage(image_data)

        return image

    # TODO: возвращать ROI для нахождения лиц
    def detect_motion(self, image_data):
        motion = self._motion_detection_model.detect_motion(image_data)

        for (x, y, w, h) in motion:
            cv2.rectangle(image_data,
                          (x, y),
                          (x + w, y + h),
                          self._colorMotion,
                          self._thickness)

    # TODO: возвращать ROI для распознавания лица
    def detect_faces(self, image_data):
        """
        Возвращает список ROI с лицами
        :param image_data: исходное изображение
        :return: список ROI с лицами
        """
        faces = self._face_detection_model.detect_faces(image_data)

        for (x, y, w, h) in faces:
            cv2.rectangle(image_data,
                          (x, y),
                          (x + w, y + h),
                          self._colorFace,
                          self._thickness)

    def __camera_model_info(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.info(message)

    def __camera_model_warn(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.warning(message)

    def __camera_model_error(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.error(message)
