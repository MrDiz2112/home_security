import os
from typing import List, Tuple

import numpy as np

import cv2
import dlib
import logging
from collections import deque

from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal

from Core import CameraManager
from Core.Data import RoiData
from Core.Utils import ImageOperations as IOps


class RecognitionThread(QThread):
    on_prepare_finished = pyqtSignal()

    def __init__(self, manager: CameraManager):
        super().__init__()

        self.__manager: CameraManager = manager
        self.__is_running: bool = False

        self.__face_rec_model: dlib.face_recognition_model_v1 = None

    def run(self):
        if self.__manager is None:
            self.__recognition_warn("Manager is null!")
            return

        self.__is_running = True

        if not self.__prepare_recognition():
            self.__recognition_warn("Preparation to recognition is failed!")
            return

        self.__recognition_info("Start recognition")
        self.on_prepare_finished.emit()

        while self.__is_running:
            self.__recognize()
            pass

        self.__recognition_info("Recognition stopped")

    def stop(self):
        self.__is_running = False
        self.__recognition_info(f"Stopping recognition")

    def __prepare_recognition(self) -> bool:
        try:
            fr_path = os.path.join(os.getcwd(), "Resources", "face_recognition_resnet.dat")

            if not os.path.exists(fr_path):
                self.__recognition_warn("Missing resource .dat files")
                return False

            self.__face_rec_model = dlib.face_recognition_model_v1(fr_path)

            self.__recognition_info("Preparation to recognition completed")
            return True

        except Exception as ex:
            self.__recognition_error(f"Error during preparation to recognition {ex}")
            return False

    def __recognize(self) -> List[RoiData]:
        """
        Возвращает дескриптор обнаруженного лица
        :return:
        """
        try:
            face_roi: RoiData = self.__manager.get_face_roi()

            img: np.ndarray = face_roi.img

            b, g, r = cv2.split(img)
            img_rgb = cv2.merge((r, g, b))

            face_desc = self.__face_rec_model.compute_face_descriptor(img_rgb, face_roi.shape)
            print(face_desc)

        except Exception as ex:
            self.__recognition_error(f"{ex}")


    def __recognition_info(self, msg:str):
        message = f"[FaceDetectionThread] {msg}"
        logging.info(message)

    def __recognition_warn(self, msg:str):
        message = f"[FaceDetectionThread] {msg}"
        logging.warning(message)

    def __recognition_error(self, msg:str):
        message = f"[FaceDetectionThread] {msg}"
        logging.error(message)
