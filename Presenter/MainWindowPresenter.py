import logging

from PyQt5.QtCore import pyqtSlot, Qt, QObject, QThread
from PyQt5.QtGui import QImage, QPixmap

from Configuration import FaceDetectionConfig
from Core import CameraManager
from Core.Threads import CameraUiThread
from Models import CameraModel

from Views import MainWindowView


class MainWindowPresenter(QObject):
    def __init__(self, view: MainWindowView):
        super().__init__()
        self.view = view

        # TODO: выбор порта
        self.__manager: CameraManager = CameraManager()

        fps = 25.0

        self.__camera_ui_thread = CameraUiThread(fps)
        self.__camera_ui_thread.assign_caller(self.__manager.get_first_camera_data)

    def start_camera(self):
        try:
            self.__presenter_info("Start init")

            is_display_processing = self.view.displayProcessingCheckBox.isChecked()
            self.__manager.start_processing()

            self.__presenter_info("Start Camera UI Thread")

            self.__camera_ui_thread.on_new_image.connect(self.__update_camera_widget_image)
            self.__camera_ui_thread.start()

            self.view.startButton.setEnabled(False)
            self.view.stopButton.setEnabled(True)
        except Exception as ex:
            self.__presenter_error(f"Cannot start camera {ex}")

    def stop_camera(self):
        try:
            self.__manager.stop_processing()
            self.__camera_ui_thread.stop()

            self.view.startButton.setEnabled(True)
            self.view.stopButton.setEnabled(False)
        except Exception as ex:
            self.__presenter_error(f"{ex}")

    def switch_mode(self):
        pass

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
