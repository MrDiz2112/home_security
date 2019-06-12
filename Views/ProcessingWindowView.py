import logging

import Views.Widgets

from PyQt5 import QtWidgets

from Core.Config import ProcessingConfig
from Presenter import ProcessingWindowPresenter

class ProcessingWindowView(QtWidgets.QDialog, Views.Widgets.ProcessingWindow):
    def __init__(self):
        super(ProcessingWindowView, self).__init__()
        self.setupUi(self)

        self.__config = ProcessingConfig()
        self.__presenter = ProcessingWindowPresenter.ProcessingWindowPresenter(self)

        self.motionCheckBox.setChecked(self.__config.detect_motion)
        self.faceCheckBox.setChecked(self.__config.detect_faces)
        self.recognitionCheckBox.setChecked(self.__config.recognize_faces)
        self.displayProcessingCheckBox.setChecked(self.__config.display_result)

        self.applyButton.clicked.connect(self.update_config)

    def update_config(self):
        self.__presenter.update_config()

    def __ui_info(self, msg:str):
        message = f"[UI] {msg}"
        logging.info(message)

    def __ui_warn(self, msg:str):
        message = f"[UI] {msg}"
        logging.warning(message)

    def __ui_error(self, msg:str):
        message = f"[UI] {msg}"
        logging.error(message)
