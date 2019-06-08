from typing import List

from Core.Config import BaseConfig
from Core.Data import CameraInfo


class CameraConfig(BaseConfig):
    def __init__(self, config_path="./Configuration/camera_config.json"):
        self.__cameras = None
        super().__init__(config_path)

        self.fps: float = self.data.fps

        self.cameras: List[CameraInfo] = []

        for camera in self.data.cameras:
            self.cameras.append(CameraInfo(camera.name, camera.source))
