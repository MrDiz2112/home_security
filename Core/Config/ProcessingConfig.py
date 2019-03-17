from Core.Config import BaseConfig


class ProcessingConfig(BaseConfig):
    def __init__(self, config_path="./configurations/processing_config.json"):
        self.__cameras = None
        super().__init__(config_path)
        self.__cameras = self.data.cameras

    @property
    def cameras(self):
        return self.__cameras
