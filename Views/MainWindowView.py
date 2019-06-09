import logging

import Views.Widgets

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Presenter import MainWindowPresenter


class MainWindowView (QtWidgets.QMainWindow, Views.Widgets.MainWindow):
    def __init__(self):
        super(MainWindowView, self).__init__()
        self.setupUi(self)

        # Поля патерна MVP
        self.__presenter = MainWindowPresenter.MainWindowPresenter(self)

        # Назначение функций
        self.startButton.clicked.connect(self.start_video)
        self.stopButton.clicked.connect(self.stop_video)
        self.databaseButton.clicked.connect(self.show_database)

        # Настройка виджетов
        self.cameraImage.setAutoFillBackground(True)
        cameraImage_palete =self.cameraImage.palette()
        cameraImage_palete.setColor(self.cameraImage.backgroundRole(), Qt.black)
        self.cameraImage.setPalette(cameraImage_palete)

    def start_video(self):
        self.__presenter.start_camera()
        self.__ui_info("Start video recording")

    def stop_video(self):
        self.__presenter.stop_camera()
        self.__ui_info("Stop video recording")

    def show_database(self):
        self.__presenter.show_database()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.__presenter.stop_camera()

    def __ui_info(self, msg:str):
        message = f"[UI] {msg}"
        logging.info(message)

    def __ui_warn(self, msg:str):
        message = f"[UI] {msg}"
        logging.warning(message)

    def __ui_error(self, msg:str):
        message = f"[UI] {msg}"
        logging.error(message)
