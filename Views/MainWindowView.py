import Views.Widgets

from PyQt5 import QtWidgets, QtCore

from Presenter import MainWindowPresenter


class MainWindowView (QtWidgets.QMainWindow, Views.Widgets.MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Вспомгательные поля
        self.timer = QtCore.QBasicTimer()

        # Поля виджетов
        self.cameraWidget = Views.Widgets.CameraWidget()
        self.cameraImageLayout.addWidget(self.cameraWidget)

        # Поля патерна MVP
        self.presenter = MainWindowPresenter(self)

        # Назначение функций
        self.startButton.clicked.connect(self.start_video)

    def start_video(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if event.timerId() != self.timer.timerId():
            return

        self.presenter.get_camera_image()

        self.update()
