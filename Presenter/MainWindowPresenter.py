import Views.Widgets
from Configuration import FaceDetectionConfig
from Models import CameraModel

from PyQt5 import QtWidgets


class MainWindowPresenter (QtWidgets.QMainWindow, Views.Widgets.MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        # self.cameraWidget = Views.Widgets.CameraWidget(FaceDetectionConfig.cascade_path)
        self.cameraWidget = Views.Widgets.CameraWidget(FaceDetectionConfig.cascade_path)
        self.cameraImageLayout.addWidget(self.cameraWidget)

        # TODO: set video port
        self.cameraModel = CameraModel()

        image_data_slot = self.cameraWidget.image_data_slot
        self.cameraModel.image_data.connect(image_data_slot)

        self.startButton.clicked.connect(self.cameraModel.start_video)
