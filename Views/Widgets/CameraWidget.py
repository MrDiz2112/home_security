import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QSizePolicy


class CameraWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        # self.image = QtGui.QImage()
