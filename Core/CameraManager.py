import logging
from typing import List

from Core.Config import CameraConfig
from Models import CameraModel


class CameraManager:
    def __init__(self, config: CameraConfig):
        super().__init__()
        self.__cameras: List[CameraModel] = []
        self.__workers = []

        for camera_info in config.cameras:
            camera = CameraModel(camera_info.name, camera_info.source, config.fps)
            self.__cameras.append(camera)

    def get_first_camera_data(self):
        return self.__cameras[0].get_actual_data()

    def start_processing(self):
        for camera in self.__cameras:
            camera.start_processing()

    def stop_processing(self):
        for camera in self.__cameras:
            camera.stop_processing()

    def __manager_info(self, msg:str):
        message = f"[Manager] {msg}"
        logging.info(message)

    def __manager_warn(self, msg:str):
        message = f"[Manager] {msg}"
        logging.warning(message)

    def __manager_error(self, msg:str):
        message = f"[Manager] {msg}"
        logging.error(message)
