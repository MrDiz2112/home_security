import logging
from typing import List, Tuple

import numpy as np

from Core.Data import RoiData
from Core.Threads import CameraThread, FrameProcessing


class CameraModel:
    def __init__(self, camera_source, fps: float):
        super().__init__()

        self.__camera_port = camera_source
        self.__fps = fps

        self.__camera_thread = CameraThread(self.__camera_port, self.__fps)
        self.__worker = FrameProcessing(str(camera_source),
                                        self.__camera_thread.get_actual_frame)

    # Методы для View

    # TODO: обработка флага отображения обработки
    def start_processing(self) -> None:
        self.__camera_thread.start()
        self.__worker.start()

        self.__camera_model_info("Started")

    def stop_processing(self):
        self.__worker.stop()
        self.__camera_thread.stop()

        self.__camera_model_info("Stopped")

    def get_actual_data(self) -> Tuple[np.ndarray, List[RoiData]]:
        return self.__camera_thread.get_actual_frame(), self.__worker.get_roi_list()

    def __camera_model_info(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.info(message)

    def __camera_model_warn(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.warning(message)

    def __camera_model_error(self, msg:str):
        message = f"[CameraModel {self.__camera_port}] {msg}"
        logging.error(message)
