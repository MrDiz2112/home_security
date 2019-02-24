import os
import sys

from PyQt5 import QtWidgets
from Views import MainWindowView


def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindowView()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
