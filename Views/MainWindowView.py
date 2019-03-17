import logging

import Views.Widgets

from PyQt5 import QtWidgets, QtCore

from Presenter import MainWindowPresenter


class MainWindowView (QtWidgets.QMainWindow, Views.Widgets.MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Поля виджетов
        self.cameraWidget = Views.Widgets.CameraWidget()
        self.cameraImageLayout.addWidget(self.cameraWidget)

        # Поля патерна MVP
        self.__presenter = MainWindowPresenter(self)

        # Назначение функций
        self.startButton.clicked.connect(self.start_video)

    def start_video(self):
        self.__presenter.start_camera()
        self.__ui_info("Start camera")

        # self.update()

    def __ui_info(self, msg:str):
        message = f"[UI] {msg}"
        logging.info(message)

    def __ui_warn(self, msg:str):
        message = f"[UI] {msg}"
        logging.warning(message)

    def __ui_error(self, msg:str):
        message = f"[UI] {msg}"
        logging.error(message)
