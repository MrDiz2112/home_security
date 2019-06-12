import ast
import logging
import time
from queue import Queue
from threading import Thread

import cv2
import dlib
import numpy as np
from PyQt5.QtCore import pyqtSignal
from scipy.spatial import distance


from Core.Config import ProcessingConfig
from Core.Data import RoiData


class RecognitionThread(Thread):
    on_prepare_finished = pyqtSignal()

    def __init__(self, frames: Queue, face_rec_model: dlib.face_recognition_model_v1):
        from Core import NotificationManager, DatabaseWorker
        super().__init__()

        self.name = "RecognitionThread"
        self.__config = ProcessingConfig()
        self.__notification_manager = NotificationManager()
        self.__db_worker = DatabaseWorker()

        self.__faces = []
        self.__thread = None
        self.__thread_started = False
        self.__new_face_delay = 3 # seconds

        self.__is_running: bool = False

        self.__frames: Queue = frames
        self.__face_rec_model: dlib.face_recognition_model_v1 = face_rec_model

    def run(self):
        self.__is_running = True
        self.__recognition_info("Recognition started")

        while self.__is_running:
            self.__recognize()

        self.__recognition_info("Recognition stopped")

    def __recognize(self):
        """
        Recognize face and return it's descriptor
        :return:
        """

        try:
            face_roi: RoiData = self.__frames.get()

            if not self.__config.recognize_faces:
                return

            img: np.ndarray = face_roi.img

            b, g, r = cv2.split(img)
            img_rgb = cv2.merge((r, g, b))

            # win = dlib.image_window()
            # win.clear_overlay()
            # win.set_image(img_rgb)
            # win.add_overlay(face_roi.shape)
            # win.wait_until_closed()

            face_desc = self.__face_rec_model.compute_face_descriptor(img_rgb, face_roi.shape)

            faces = self.__db_worker.select_all_faces()

            wrong_face = True

            for face in faces:
                desc: str = face[3]
                values = [float(x) for x in desc.split('\n')]
                vector = dlib.vector(values)

                faces_dist = distance.euclidean(face_desc, vector)

                if faces_dist < 0.6:
                    wrong_face = False
                    break

            if wrong_face:
                if len(self.__faces) < 5:
                    self.__faces.append(img)

                if not self.__thread_started:
                    self.__thread_started = True
                    self.__thread = Thread(target=self.__send_notification)
                    self.__thread.name = "NotificationThread"
                    self.__thread.start()

        except Exception as ex:
            self.__recognition_error(f"{ex}")

    def __send_notification(self):
        while True:
            before_sleep_len = len(self.__faces)

            time.sleep(self.__new_face_delay)

            if len(self.__faces) == before_sleep_len:
                break

        self.__notification_manager.send_notifications('recognize', self.__faces[:])
        self.__faces = []
        self.__thread_started = False

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
