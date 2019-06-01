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


class FaceDetectionThread(QThread):
    on_prepare_finished = pyqtSignal()

    def __init__(self, manager: CameraManager):
        super().__init__()

        self.__manager: CameraManager = manager
        self.__is_running: bool = False

        self.__shape_predictor = None
        self.__face_rec_model = None
        self.__detector = dlib.get_frontal_face_detector()

        self.__faces_roi: List[RoiData] = []

        self.__frames_count = 0

    def run(self):
        if self.__manager is None:
            self.__face_thread_warn("Manager is null!")
            return

        self.__is_running = True

        if not self.__prepare_face_detection():
            self.__face_thread_warn("Preparation to motion detection is failed!")
            return

        self.__face_thread_info("Start face detection")
        self.on_prepare_finished.emit()

        while self.__is_running:
            faces = self.__detect_face()
            self.__frames_count += 1

            self.__manager.put_face_roi(faces)
            pass

        self.__face_thread_info("Motion detection stopped")

    def stop(self):
        self.__is_running = False
        self.__face_thread_info(f"Stopping motion detection")

    def __prepare_face_detection(self) -> bool:
        try:
            sp_path = os.path.join(os.getcwd(), "Resources", "face_shape_predictor.dat")
            fr_path = os.path.join(os.getcwd(), "Resources", "face_recognition_resnet.dat")

            if not os.path.exists(sp_path) and not os.path.exists(fr_path):
                self.__face_thread_info("Missing resource .dat files")
                return False

            self.__shape_predictor = dlib.shape_predictor(sp_path)
            self.__face_rec_model = dlib.face_recognition_model_v1(fr_path)

            self.__face_thread_info("Preparation to motion detection completed")
            return True

        except Exception as ex:
            self.__face_thread_error(f"Error during preparation to face detection {ex}")
            return False

    def __detect_face(self) -> List[RoiData]:
        """
        Возвращает ROI, где было обнаружено лицо
        :return:
        """
        self.__faces_roi = []
        try:
            # TODO: если выключена обработка - возвращать весь кадр
            motion_roi: RoiData = self.__manager.get_motion_roi()

            x = motion_roi.roi[0]
            y = motion_roi.roi[1]

            img: np.ndarray = motion_roi.img

            # filename = os.path.join(os.getcwd(), "roi", str(self.__frames_count) + ".jpg")
            # cv2.imwrite(filename, img)

            b,g,r = cv2.split(img)
            img_rgb = cv2.merge((r,g,b))

            dets = self.__detector(img_rgb, 1)

            #TODO: расчитать смещение roi

            for k, d in enumerate(dets):
                shape : dlib.full_object_detection = self.__shape_predictor(img_rgb, d)
                roi: dlib.rectangle = shape.rect

                x_offset = x
                y_offset = y

                img_roi = img[roi.top():roi.bottom(), roi.left():roi.right()]
                face_roi = RoiData(img_roi, (x_offset + roi.left(),
                                             y_offset + roi.top(),
                                             roi.right() - roi.left(),
                                             roi.bottom() - roi.top()))

                # filename = os.path.join(os.getcwd(), "roi", "f_" + str(self.__frames_count) + ".jpg")
                # cv2.imwrite(filename, img_roi)

                self.__faces_roi.append(face_roi)
        except Exception as ex:
            self.__face_thread_error(f"{ex}")

        return self.__faces_roi


    def __face_thread_info(self, msg:str):
        message = f"[FaceDetectionThread] {msg}"
        logging.info(message)

    def __face_thread_warn(self, msg:str):
        message = f"[FaceDetectionThread] {msg}"
        logging.warning(message)

    def __face_thread_error(self, msg:str):
        message = f"[FaceDetectionThread] {msg}"
        logging.error(message)
