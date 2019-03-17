import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QSizePolicy


class CameraWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image :QPixmap = QPixmap()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # def paintEvent(self, event):
    #     painter = QtGui.QPainter(self)
    #     painter.drawImage(0, 0, self.image)
    #     # self.image = QtGui.QImage()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.image)
