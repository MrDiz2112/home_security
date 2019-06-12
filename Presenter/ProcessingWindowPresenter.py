import logging

from Core.Config import ProcessingConfig


class ProcessingWindowPresenter:
    def __init__(self, view):
        self.__view = view

        self.__config = ProcessingConfig()

    def update_config(self):
        try:
            detect_motion = self.__view.motionCheckBox.isChecked()
            detect_faces = self.__view.faceCheckBox.isChecked()
            recognize = self.__view.recognitionCheckBox.isChecked()
            display = self.__view.displayProcessingCheckBox.isChecked()

            self.__config.detect_motion = detect_motion
            self.__config.detect_faces = detect_faces
            self.__config.recognize_faces = recognize
            self.__config.display_result = display

            self.__config.update_config()
        except Exception as ex:
            self.__presenter_error(f"{ex}")

        self.__view.close()

    def __presenter_info(self, msg: str):
        message = f"[ProcessingWindowPresenter] {msg}"
        logging.info(message)

    def __presenter_warn(self, msg: str):
        message = f"[ProcessingWindowPresenter] {msg}"
        logging.warning(message)

    def __presenter_error(self, msg: str):
        message = f"[ProcessingWindowPresenter] {msg}"
        logging.error(message)