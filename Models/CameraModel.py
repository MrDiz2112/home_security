from typing import List

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui

from Models import FaceDetectionModel, MotionDetectionModel


class CameraModel(QtCore.QObject):
    def __init__(self, cascade_filepath: str, camera_port: int = 0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)

        self._colorFace = (0, 255, 182)
        self._colorMotion = (0, 0, 255)
        self._thickness = 2

        self._face_detection_model = FaceDetectionModel(cascade_filepath)
        self._motion_detection_model = MotionDetectionModel()

    # Методы для View

    def get_camera_image(self, is_display_processing: bool) -> QtGui.QImage:
        """
        Возвращает изображение с камеры
        :param is_display_processing: отображать ли результат обработки
        :return: изображение с камеры
        """
        read, data = self.camera.read()

        # TODO: обработка изображения в независимости от выбора
        if read:
            if is_display_processing:
                return self.process_image_data(data)
            else:
                return self.get_qimage(data)

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

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image
