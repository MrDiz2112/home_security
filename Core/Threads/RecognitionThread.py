import os
from queue import Queue
from threading import Thread
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


class RecognitionThread(Thread):
    on_prepare_finished = pyqtSignal()

    def __init__(self, frames: Queue, face_rec_model: dlib.face_recognition_model_v1):
        super().__init__()

        self.__is_running: bool = False

        self.__frames: Queue = frames
        self.__face_rec_model: dlib.face_recognition_model_v1 = face_rec_model

    def run(self):
        self.name = "RecognitionThread"

        self.__is_running = True
        self.__recognition_info("Recognition started")

        while self.__is_running:
            self.__recognize()

        self.__recognition_info("Recognition stopped")

    def __recognize(self):
        """
        Возвращает дескриптор обнаруженного лица
        :return:
        """
        try:
            face_roi: RoiData = self.__frames.get()

            img: np.ndarray = face_roi.img

            b, g, r = cv2.split(img)
            img_rgb = cv2.merge((r, g, b))

            face_desc = self.__face_rec_model.compute_face_descriptor(img_rgb, face_roi.shape)
            print(face_desc)

        except Exception as ex:
            self.__recognition_error(f"{ex}")

    def stop(self):
        self.__is_running = False

    def __recognition_info(self, msg:str):
        message = f"[FaceDetectionThread] {msg}"
        logging.info(message)

    def __recognition_warn(self, msg:str):
        message = f"[FaceDetectionThread] {msg}"
        logging.warning(message)

    def __recognition_error(self, msg:str):
        message = f"[FaceDetectionThread] {msg}"
        logging.error(message)
