import logging
from typing import List

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

from Core import CameraManager
from Core.Threads import CameraThread, MotionDetectionThread
from Models import FaceDetectionModel, MotionDetectionModel


class CameraModel(QtCore.QObject):
    on_camera_thread_finished = pyqtSignal()

    def __init__(self, cascade_filepath: str, camera_port: int, fps: float, manager: CameraManager):
        super().__init__()

        self.__manager = manager
        self.__camera_port = camera_port
        self.__fps = fps

        self.__camera_thread = CameraThread(self.__camera_port, self.__fps, self.__manager)
        self.__motion_detection_thread = MotionDetectionThread(self.__manager, 5)

        self.__camera_thread.finished.connect(self.__grab_finished)
        self.__motion_detection_thread.finished.connect(self.__motion_detection_finished)

        self._face_detection_model = FaceDetectionModel(cascade_filepath)
        self._motion_detection_model = MotionDetectionModel()

    # Методы для View

    # TODO: обработка флага отображения обработки
    def start_processing(self, is_display_processing: bool) -> None:
        self.__camera_thread.start(QThread.HighestPriority)
        self.__motion_detection_thread.start(QThread.HighPriority)

    def stop_processing(self):
        self.__motion_detection_thread.stop()
        self.__camera_thread.stop()

    @pyqtSlot()
    def __grab_finished(self):
        self.__camera_model_info("Frame grabber finished")
        self.on_camera_thread_finished.emit()

    @pyqtSlot()
    def __motion_detection_finished(self):
        self.__camera_model_info("Motion Detection finished")

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

    # TODO: нет ссылок
    def __draw_rectangle(self, cnt, img):
        x, y, w, h = cv2.boundingRect(cnt)

        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(img, (cx, cy), 3, (255, 255, 0), 3)

    def __camera_model_info(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.info(message)

    def __camera_model_warn(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.warning(message)

    def __camera_model_error(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.error(message)
