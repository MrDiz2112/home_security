import logging

import Views.Widgets

from PyQt5 import QtWidgets
from Presenter import FacesWindowPresenter


class FacesWindowView(QtWidgets.QDialog, Views.Widgets.FacesWindow):
    def __init__(self):
        super(FacesWindowView, self).__init__()
        self.setupUi(self)

        self.__presenter = FacesWindowPresenter.FacesWindowPresenter(self)

        self.addButton.clicked.connect(self.add_face)
        self.deleteButton.clicked.connect(self.delete_face)

        self.__presenter.fill_table()

    def add_face(self):
        self.__presenter.add_face()

    def delete_face(self):
        self.__presenter.delete_face()

    def fill_table(self):
        self.__presenter.fill_table()

    def __ui_info(self, msg:str):
        message = f"[UI] {msg}"
        logging.info(message)

    def __ui_warn(self, msg:str):
        message = f"[UI] {msg}"
        logging.warning(message)

    def __ui_error(self, msg:str):
        message = f"[UI] {msg}"
        logging.error(message)