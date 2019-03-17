import logging

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap

from Configuration import FaceDetectionConfig
from Core import Manager
from Core.Threads import CameraUiThread
from Models import CameraModel

from Views import MainWindowView


class MainWindowPresenter:
    def __init__(self, view : MainWindowView):

        self.view = view

        # TODO: выбор порта
        self.__manager: Manager = Manager()

        fps = 25.0

        self.__cameraModel = CameraModel(FaceDetectionConfig.cascade_path, r"materials/thief1.mp4", fps, self.__manager)

        self.__camera_ui_thread = CameraUiThread()

    def start_camera(self):
        self.__presenter_info("Start camera init")

        is_display_processing = self.view.displayProcessingCheckBox.isChecked()
        self.__cameraModel.start_frame_grabber(is_display_processing)

        self.__presenter_info("Start Camera UI Thread")

        self.__camera_ui_thread.assign_caller(self.__manager.get_camera_image)
        self.__camera_ui_thread.on_new_image.connect(self.__update_camera_widget_image)
        self.__camera_ui_thread.start()

    @pyqtSlot(QImage)
    def __update_camera_widget_image(self, image):
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(self.view.cameraImage.width(), self.view.cameraImage.height(), Qt.KeepAspectRatio)

        self.view.cameraImage.setPixmap(pixmap)

        # if self.view.cameraWidget.image.size() != self.view.cameraWidget.size():
        #     self.view.cameraWidget.image.setFixedSize(self.view.cameraWidget.size())

        # self.view.cameraImage = self.view.cameraImage.scaled(self.view.cameraWidget.image.width(),
        #                                                                    self.view.cameraWidget.image.height(),
        #                                                                    Qt.KeepAspectRatio)

        self.view.update()

    def switch_mode(self):
        pass

    def __presenter_info(self, msg:str):
        message = f"[MainWindowPresenter] {msg}"
        logging.info(message)

    def __presenter_warn(self, msg:str):
        message = f"[MainWindowPresenter] {msg}"
        logging.warning(message)

    def __presenter_error(self, msg:str):
        message = f"[MainWindowPresenter] {msg}"
        logging.error(message)
