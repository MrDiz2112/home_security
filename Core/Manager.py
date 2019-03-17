import logging

import numpy as np

from queue import Queue


class Manager:
    def __init__(self):
        self.__camera_frames: Queue = Queue()
        self.__processed_frames: Queue = Queue()

    # TODO: добавить поддержку аннотаций
    # TODO: своровать у Данила Visualisation.py
    def get_camera_image(self):
        img = self.__camera_frames.get()

        return img

    def get_processed_image(self):
        img = self.__processed_frames.get()

        return img

    def put_frame(self, img:np.ndarray):
        self.__camera_frames.put(img)

    def clear_manager(self):
        while not self.__camera_frames.empty():
            self.__camera_frames.get()

        self.__manager_info("Camera frames queue cleared")

        while not self.__processed_frames.empty():
            self.__processed_frames.get()

        self.__manager_info("Processed frames queue cleared")

    def __manager_info(self, msg:str):
        message = f"[Manager] {msg}"
        logging.info(message)

    def __manager_warn(self, msg:str):
        message = f"[Manager] {msg}"
        logging.warning(message)

    def __manager_error(self, msg:str):
        message = f"[Manager] {msg}"
        logging.error(message)
