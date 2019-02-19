from PyQt5 import QtWidgets

from Views.Widgets import MainWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, haar_cascade_filepath):
        super().__init__()

        self.main_widget = MainWidget(haar_cascade_filepath)

        self.setCentralWidget(self.main_widget)
