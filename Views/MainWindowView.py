import Views.Widgets
from Configuration import FaceDetectionConfig

from PyQt5 import QtWidgets

from Presenter import MainWindowPresenter


class MainWindowView (QtWidgets.QMainWindow, Views.Widgets.MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        # self.cameraWidget = Views.Widgets.CameraWidget(FaceDetectionConfig.cascade_path)
        self.cameraWidget = Views.Widgets.CameraWidget(FaceDetectionConfig.cascade_path)
        self.cameraImageLayout.addWidget(self.cameraWidget)

        self.presenter = MainWindowPresenter(self)
