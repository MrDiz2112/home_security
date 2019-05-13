from typing import List, Tuple

import cv2
import numpy as np
from PyQt5.QtCore import QObject


class FaceDetectionModel(QObject):
    def __init__(self, cascade_filepath: str):
        super().__init__()
        self.classifier = cv2.CascadeClassifier(cascade_filepath)
        self._min_size = (15, 15)

    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Ищет лица на изображении
        :param image: исходное изображение
        :return: список координат (x, y, w, h), где найдены лица
        """
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=self._min_size)

        return faces
