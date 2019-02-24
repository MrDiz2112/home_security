from Configuration import FaceDetectionConfig
from Models import CameraModel

from Views import MainWindowView


class MainWindowPresenter:
    def __init__(self, view : MainWindowView):

        self.view = view

        # TODO: выбор порта
        self.cameraModel = CameraModel(FaceDetectionConfig.cascade_path, r"materials/thief1.mp4")

    def get_camera_image(self):
        is_display_processing = self.view.displayProcessingCheckBox.isChecked()

        image = self.cameraModel.get_camera_image(is_display_processing)

        self.view.cameraWidget.image = image

        if self.view.cameraWidget.image.size() != self.view.cameraWidget.size():
            self.view.cameraWidget.setFixedSize(self.view.cameraWidget.image.size())
