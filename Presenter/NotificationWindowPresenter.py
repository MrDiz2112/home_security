import logging

from Core.Config import NotificationConfig


class NotificationWindowPresenter:
    def __init__(self, view):
        self.__view = view

        self.__config = NotificationConfig()

    def update_config(self):
        try:
            notify_email = self.__view.emailCheckBox.isChecked()
            notify_telegram = self.__view.telegramCheckBox.isChecked()
            email = self.__view.emailLineEdit.text()
            password = self.__view.passwordLineEdit.text()
            bot_key = self.__view.telegramLineEdit.text()

            self.__config.notify_email = notify_email
            self.__config.notify_telegram = notify_telegram
            self.__config.email = email
            self.__config.password = password
            self.__config.bot_key = bot_key

            self.__config.update_config()
        except Exception as ex:
            self.__presenter_error(f"{ex}")

        self.__view.close()

    def __presenter_info(self, msg: str):
        message = f"[ProcessingWindowPresenter] {msg}"
        logging.info(message)

    def __presenter_warn(self, msg: str):
        message = f"[ProcessingWindowPresenter] {msg}"
        logging.warning(message)

    def __presenter_error(self, msg: str):
        message = f"[ProcessingWindowPresenter] {msg}"
        logging.error(message)