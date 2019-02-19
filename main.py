import os
import sys

from PyQt5 import QtWidgets
from Views import MainWindow


def launch(haar_cascade_filepath):
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(haar_cascade_filepath)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    cascade_filepath = os.path.join('haarcascade_frontalface_default.xml')

    cascade_filepath = os.path.abspath(cascade_filepath)
    launch(cascade_filepath)