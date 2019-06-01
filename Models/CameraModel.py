import logging
from typing import List

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

from Core import CameraManager
from Core.Threads import CameraThread, MotionDetectionThread, FaceDetectionThread, RecognitionThread
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
        self.__face_detection_thread = FaceDetectionThread(self.__manager)
        self.__recognition_thread = RecognitionThread(self.__manager)

        self.__camera_thread.finished.connect(self.__grab_finished)
        self.__motion_detection_thread.finished.connect(self.__motion_detection_finished)
        self.__face_detection_thread.finished.connect(self.__face_detection_finished)
        self.__recognition_thread.finished.connect(self.__recognition_finished)

        self.__face_detection_thread.on_prepare_finished.connect(self.__launch_camera)
        self.__recognition_thread.on_prepare_finished.connect(self.__prepare_face_detection)

    # Методы для View

    # TODO: обработка флага отображения обработки
    def start_processing(self, is_display_processing: bool) -> None:
        self.__recognition_thread.start()

    def __prepare_face_detection(self):
        self.__face_detection_thread.start(QThread.HighestPriority)

    def stop_processing(self):
        self.__recognition_thread.stop()
        self.__face_detection_thread.stop()
        self.__motion_detection_thread.stop()
        self.__camera_thread.stop()

    @pyqtSlot()
    def __launch_camera(self):
        self.__camera_thread.start(QThread.IdlePriority)
        self.__motion_detection_thread.start(QThread.HighestPriority)

    @pyqtSlot()
    def __grab_finished(self):
        self.__camera_model_info("Frame grabber finished")
        self.on_camera_thread_finished.emit()

    @pyqtSlot()
    def __motion_detection_finished(self):
        self.__camera_model_info("Motion Detection finished")

    @pyqtSlot()
    def __face_detection_finished(self):
        self.__camera_model_info("Face Detection finished")

    @pyqtSlot()
    def __recognition_finished(self):
        self.__camera_model_info("Recognition finished")

    def __camera_model_info(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.info(message)

    def __camera_model_warn(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.warning(message)

    def __camera_model_error(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.error(message)
