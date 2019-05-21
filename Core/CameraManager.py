import asyncio
import logging
from typing import List, Tuple

import cv2
import numpy as np

from queue import Queue

from Core.Data import RoiData


class CameraManager:
    def __init__(self):
        self.__camera_frames: Queue = Queue()
        self.__motions_roi: Queue = Queue()
        self.__faces_roi: Queue = Queue()

        self.__motions_roi_to_draw: List[Tuple[int, int, int, int]] = []
        self.__faces_roi_to_draw: List[Tuple[int, int, int, int]] = []

        self.__color_motion = (0, 0, 255)
        self.__color_face = (0, 255, 182)
        self.__thickness = 2

    # TODO: добавить поддержку аннотаций
    # TODO: своровать у Данила Visualisation.py
    def get_camera_image(self) -> np.ndarray:
        img = self.__camera_frames.get()

        self.__draw_rect(img, self.__motions_roi_to_draw, self.__color_motion)
        self.__draw_rect(img, self.__faces_roi_to_draw, self.__color_face)

        return img

    def __draw_rect(self, img: np.ndarray, roi: List[Tuple[int, int, int, int]], color: Tuple[int, int, int]):
        if len(roi) != 0:
            for motion_roi in roi:
                try:
                    x,y,w,h = motion_roi
                    if  x >= 0 and y >= 0 and w >= 0 and h >= 0:
                        cv2.rectangle(img, (x,y), (x+w, y+h), color, self.__thickness)
                except Exception as ex:
                    self.__manager_error(f"Failed to draw rect. {ex}")

            roi.clear()

    def get_motion_roi(self) -> RoiData:
        img = self.__motions_roi.get()

        return img

    def get_face_image(self) -> np.ndarray:
        img = self.__faces_roi.get()

        return img

    def put_camera_frame(self, img:np.ndarray):
        self.__camera_frames.put(img)

    def put_motion_roi(self, motion_roi: RoiData):
        self.__motions_roi.put(motion_roi)

        self.__motions_roi_to_draw.append(motion_roi.roi)

    def put_face_roi(self, face_roi: RoiData):
        self.__faces_roi.put(face_roi)

        self.__faces_roi_to_draw.append(face_roi.roi)

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
