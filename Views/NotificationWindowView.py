import logging

import Views.Widgets

from PyQt5 import QtWidgets

from Core.Config import NotificationConfig
from Presenter import NotificationWindowPresenter

class NotificationWindowView(QtWidgets.QDialog, Views.Widgets.NotificationWindow):
    def __init__(self):
        super(NotificationWindowView, self).__init__()
        self.setupUi(self)

        self.__config = NotificationConfig()
        self.__presenter = NotificationWindowPresenter.NotificationWindowPresenter(self)

        self.emailCheckBox.setChecked(self.__config.notify_email)
        self.telegramCheckBox.setChecked(self.__config.notify_telegram)

        self.emailLineEdit.setText(self.__config.email)
        self.passwordLineEdit.setText(self.__config.password)
        self.telegramLineEdit.setText(self.__config.bot_key)

        self.applyButton.clicked.connect(self.update_config)

    def update_config(self):
        self.__presenter.update_config()

    def __ui_info(self, msg:str):
        message = f"[UI] {msg}"
        logging.info(message)

    def __ui_warn(self, msg:str):
        message = f"[UI] {msg}"
        logging.warning(message)

    def __ui_error(self, msg:str):
        message = f"[UI] {msg}"
        logging.error(message)
