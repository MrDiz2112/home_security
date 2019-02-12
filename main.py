from PyQt5.QtWidgets import QApplication

from Models import CameraModel
from Views import MainWindow

camera = CameraModel(0)
camera.initialize()

app = QApplication([])
start_window = MainWindow(camera)
start_window.show()
app.exit(app.exec_())