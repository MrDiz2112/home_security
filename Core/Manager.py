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
