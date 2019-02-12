from PyQt5.QtCore import QThread


class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
