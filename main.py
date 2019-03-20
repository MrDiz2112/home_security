import os
import sys
import logging

from datetime import datetime
from PyQt5 import QtWidgets
from Views import MainWindowView


def main():
    now_date = datetime.now()

    init_logger(now_date)

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindowView()
    main_window.show()

    logging.info("[Main] Application started!")

    sys.exit(app.exec_())


def init_logger(now_date):
    if not os.path.isdir("./log"):
        os.makedirs("./log")

    # log_formatter = logging.Formatter('[%(asctime)s][%(threadName)s][%(levelname)s] %(message)s')
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s]%(message)s')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    file_handler_name = f"./log/HomeSecurity-{now_date.strftime('%Y-%m-%d')}.log"

    if os.path.isfile(file_handler_name):
        os.remove(file_handler_name)

    file_handler = logging.FileHandler(file_handler_name)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)


if __name__ == '__main__':
    main()
