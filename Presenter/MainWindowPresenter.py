from Models import CameraModel

from Views import MainWindowView


class MainWindowPresenter:
    def __init__(self, view : MainWindowView):

        self.view = view

        # TODO: set video port
        self.cameraModel = CameraModel()

        image_data_slot = view.cameraWidget.image_data_slot
        self.cameraModel.image_data.connect(image_data_slot)

        view.startButton.clicked.connect(self.cameraModel.start_video)
