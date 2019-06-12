import json

from Core.Config import BaseConfig


class ProcessingConfig(BaseConfig):
    def __init__(self, config_path="./Configuration/processing_config.json"):
        super().__init__(config_path)
        self.detect_motion = self.data.detect_motion
        self.detect_faces = self.data.detect_faces
        self.recognize_faces = self.data.recognize_faces
        self.display_result = self.data.display_result
