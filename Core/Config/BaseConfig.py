import json
from types import SimpleNamespace as Namespace
import os


class BaseConfig:
    def __init__(self, config_path):
        if config_path is None:
            raise ValueError("Config path is null")

        if not os.path.isfile(config_path):
            raise ValueError("Invalid config path")

        with open(config_path) as f:
            self.data = json.load(f, object_hook=lambda d: Namespace(**d))
