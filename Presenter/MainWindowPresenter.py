import logging

from PyQt5.QtCore import pyqtSlot, Qt, QObject, QThread
from PyQt5.QtGui import QImage, QPixmap

from Core import CameraManager
from Core.Config import CameraConfig
from Core.Threads import CameraUiThread
from Models import CameraModel

from Views import MainWindowView, FacesWindowView, ProcessingWindowView


class MainWindowPresenter(QObject):
    def __init__(self, view: MainWindowView):
        super().__init__()
        self.view = view

        # TODO: выбор порта
        self.__camera_config = CameraConfig()

        self.__manager: CameraManager = CameraManager(self.__camera_config)

        self.__camera_ui_thread = None

    def start_camera(self):
        try:
            self.__presenter_info("Start init")

            self.__manager.start_processing()

            self.__presenter_info("Start Camera UI Thread")

            self.__camera_ui_thread = CameraUiThread(self.__camera_config.fps)
            self.__camera_ui_thread.assign_caller(self.__manager.get_first_camera_data)

            self.__camera_ui_thread.on_new_image.connect(self.__update_camera_widget_image)
            self.__camera_ui_thread.start()

            self.view.startButton.setEnabled(False)
            self.view.stopButton.setEnabled(True)

            self.view.databaseButton.setEnabled(False)
            self.view.settingsButton.setEnabled(False)
        except Exception as ex:
            self.__presenter_error(f"Cannot start camera {ex}")

    def stop_camera(self):
        try:
            self.__camera_ui_thread.stop()
            self.__manager.stop_processing()

            self.view.startButton.setEnabled(True)
            self.view.stopButton.setEnabled(False)

            self.view.databaseButton.setEnabled(True)
            self.view.settingsButton.setEnabled(True)
        except Exception as ex:
            self.__presenter_error(f"{ex}")

    def show_database(self):
        try:
            database = FacesWindowView.FacesWindowView()
            database.exec_()
        except Exception as ex:
            self.__presenter_error(f"Failed to open database. {ex}")

    def show_processing_window(self):
        try:
            processing_window = ProcessingWindowView.ProcessingWindowView()
            processing_window.exec_()
        except Exception as ex:
            self.__presenter_error(f"{ex}")

    @pyqtSlot(QImage)
    def __update_camera_widget_image(self, image):
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(self.view.cameraImage.width(), self.view.cameraImage.height(), Qt.KeepAspectRatio)

        self.view.cameraImage.setPixmap(pixmap)
        self.view.update()

    @pyqtSlot()
    def __reset_camera(self):
        self.view.startButton.setEnabled(True)
        self.view.stopButton.setEnabled(False)

    def __presenter_info(self, msg:str):
        message = f"[MainWindowPresenter] {msg}"
        logging.info(message)

    def __presenter_warn(self, msg:str):
        message = f"[MainWindowPresenter] {msg}"
        logging.warning(message)

    def __presenter_error(self, msg:str):
        message = f"[MainWindowPresenter] {msg}"
        logging.error(message)
