from typing import List

from Core.Config import BaseConfig
from Core.Data import CameraInfo


class ResourcesConfig(BaseConfig):
    def __init__(self, config_path="./Configuration/resources_config.json"):
        self.shape_predictor = ""
        self.recognition_resnet =""
        super().__init__(config_path)

        self.shape_predictor: str = self.data.shape_predictor
        self.recognition_resnet: str = self.data.recognition_resnet
