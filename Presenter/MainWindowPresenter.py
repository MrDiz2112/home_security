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

        self.__camera_ui_thread = CameraUiThread()
        self.__cameraModel = CameraModel(FaceDetectionConfig.cascade_path,
                                         r"materials/thief1.mp4",
                                         fps,
                                         self.__manager)

        self.__cameraModel.on_thread_finished.connect(self.__reset_camera)

    def start_camera(self):
        self.__presenter_info("Start camera init")

        is_display_processing = self.view.displayProcessingCheckBox.isChecked()
        self.__cameraModel.start_frame_grabber(is_display_processing)

        self.__presenter_info("Start Camera UI Thread")

        self.__camera_ui_thread.assign_caller(self.__manager.get_camera_image)
        self.__camera_ui_thread.on_new_image.connect(self.__update_camera_widget_image)
        self.__camera_ui_thread.start()

        self.view.startButton.setEnabled(False)
        self.view.stopButton.setEnabled(True)

    def stop_camera(self):
        self.__cameraModel.stop_frame_grabber()

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
        self.__manager.clear_manager()

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
