import asyncio
import logging
from typing import List, Tuple

import cv2
import numpy as np

from queue import Queue

from PyQt5.QtCore import QObject, pyqtSignal

from Core.Data import RoiData


class CameraManager(QObject):
    on_motion_roi_changed = pyqtSignal()
    on_faces_roi_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__camera_frames: Queue = Queue()
        self.__motions_roi: Queue = Queue()
        self.__faces_roi: Queue = Queue()

        self.__motions_roi_to_draw: List[Tuple[int, int, int, int]] = []
        self.__faces_roi_to_draw: List[Tuple[int, int, int, int]] = []

    def get_camera_image(self) -> np.ndarray:
        img = self.__camera_frames.get()

        return img

    def get_motions_roi_to_draw(self):
        return self.__motions_roi_to_draw

    def get_faces_roi_to_draw(self):
        return self.__faces_roi_to_draw

    def clear_motions_roi_to_draw(self):
        self.__motions_roi_to_draw.clear()

    def clear_faces_roi_to_draw(self):
        self.__faces_roi_to_draw.clear()

    def get_motion_roi(self) -> RoiData:
        img = self.__motions_roi.get()

        return img

    def get_face_image(self) -> np.ndarray:
        img = self.__faces_roi.get()

        return img

    def put_camera_frame(self, img:np.ndarray):
        self.__camera_frames.put(img)

    def put_motion_roi(self, motion_roi: List[RoiData]):
        for roi in motion_roi:
            self.__motions_roi.put(roi)
            self.__motions_roi_to_draw.append(roi.roi)

        self.on_motion_roi_changed.emit()

    def put_face_roi(self, face_roi: List[RoiData]):
        for roi in face_roi:
            self.__faces_roi.put(roi)
            self.__faces_roi_to_draw.append(roi.roi)

        self.on_faces_roi_changed.emit()

    def clear_manager(self):
        while not self.__camera_frames.empty():
            self.__camera_frames.get()

        self.__manager_info("Camera frames queue cleared")

        while not self.__motions_roi.empty():
            self.__motions_roi.get()

        self.__manager_info("Motion frames queue cleared")

        # while not self.__faces_roi.empty():
        #     self.__faces_roi.get()

        self.__manager_info("Face frames queue cleared")

    def __manager_info(self, msg:str):
        message = f"[Manager] {msg}"
        logging.info(message)

    def __manager_warn(self, msg:str):
        message = f"[Manager] {msg}"
        logging.warning(message)

    def __manager_error(self, msg:str):
        message = f"[Manager] {msg}"
        logging.error(message)
