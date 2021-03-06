import logging
import os
import sys

from PyQt5 import QtWidgets
from datetime import datetime

from Core import NotificationManager
from Core.DatabaseWorker import DatabaseWorker
from Views import MainWindowView, FacesWindowView


def main():
    now_date = datetime.now()

    init_logger(now_date)

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindowView.MainWindowView()
    main_window.show()

    logging.info("[Main] Application started!")

    sys.exit(app.exec_())


def init_logger(now_date):
    if not os.path.isdir("./log"):
        os.makedirs("./log")

    # log_formatter = logging.Formatter('[%(asctime)s][%(threadName)s][%(levelname)s] %(message)s')
    log_formatter = logging.Formatter('[%(asctime)s][%(levelname)s]%(message)s')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    file_handler_name = f"./log/HomeSecurity-{now_date.strftime('%Y-%m-%d')}.log"

    if os.path.isfile(file_handler_name):
        os.remove(file_handler_name)

    file_handler = logging.FileHandler(file_handler_name)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    db_worker = DatabaseWorker()
    db_worker.create_db()

if __name__ == '__main__':
    main()
