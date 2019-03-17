import logging
import numpy as np
from typing import Callable

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage


class CameraUiThread(QThread):
    on_new_image = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()

        self.__is_running = False
        self.__get_frame: Callable[[], np.ndarray] = None

    def assign_caller(self, method: Callable[[], np.ndarray]):
        self.__ui_thread_info(f"Assigned caller {method.__name__}")
        self.__get_frame = method

    def run(self):
        self.__is_running = True

        self.__ui_thread_info("Start Camera UI thread")

        while self.__is_running:
            frame = self.__get_frame()

            image = self.__get_qimage(frame)

            self.on_new_image.emit(image)

    def __get_qimage(self, image: np.ndarray) -> QImage:
        """
        Преобразует изображение из формата numpy в QImage
        """
        height, width, colors = image.shape
        bytesPerLine = 3 * width

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def __ui_thread_info(self, msg:str):
        message = f"[UI Thread] {msg}"
        logging.info(message)

    def __ui_thread_warn(self, msg:str):
        message = f"[UI Thread] {msg}"
        logging.warning(message)

    def __ui_thread_error(self, msg:str):
        message = f"[UI Thread] {msg}"
        logging.error(message)
