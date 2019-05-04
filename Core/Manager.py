import logging

import numpy as np

from queue import Queue


class Manager:
    def __init__(self):
        self.__camera_frames: Queue = Queue()
        self.__motion_frames: Queue = Queue()
        self.__face_frames: Queue = Queue()

    # TODO: добавить поддержку аннотаций
    # TODO: своровать у Данила Visualisation.py
    def get_camera_image(self) -> np.ndarray:
        img = self.__camera_frames.get()

        return img

    def get_motion_image(self) -> np.ndarray:
        img = self.__motion_frames.get()

        return img

    def get_face_image(self) -> np.ndarray:
        img = self.__face_frames.get()

        return img

    def put_camera_frame(self, img:np.ndarray):
        self.__camera_frames.put(img)

    def clear_manager(self):
        while not self.__camera_frames.empty():
            self.__camera_frames.get()

        self.__manager_info("Camera frames queue cleared")

        while not self.__motion_frames.empty():
            self.__motion_frames.get()

        self.__manager_info("Motion frames queue cleared")

        while not self.__face_frames.empty():
            self.__face_frames.get()

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
