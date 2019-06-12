from typing import List

from Core.Config import BaseConfig
from Core.Data import CameraInfo


class NotificationConfig(BaseConfig):
    def __init__(self, config_path="./Configuration/notification_config.json"):
        super().__init__(config_path)

        self.notify_email: str = self.data.notify_email
        self.notify_telegram: str = self.data.notify_telegram
        self.email: str = self.data.email
        self.password: str = self.data.password
        self.bot_key: str = self.data.bot_key
