import logging
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import List
import requests

import cv2
import numpy as np
from PIL import Image
from Core.Config import NotificationConfig

HOST = "smtp.gmail.com"

class NotificationManager:
    def __init__(self):
        self.__config = NotificationConfig()
        self.__server = smtplib.SMTP(HOST, 587)

    def send_notifications(self, notify_type: str, img_list: List[np.ndarray]):
        telegram_msg = ''

        if self.__config.notify_email:
            try:
                SUBJECT = "Уведомление охранной системы"
                TO = f"{self.__config.email}"
                FROM = f"HomeSecuritySystem"

                msg = MIMEMultipart()
                telegram_msg = ""

                msg['From'] = FROM
                msg['To'] = TO
                msg['Subject'] = SUBJECT
                msg['Date'] = formatdate(localtime=True)

                if notify_type == "motion":
                    msg.attach(MIMEText("Система засекла движение!"))
                    telegram_msg = "Система засекла движение! Проверьте почту!"

                if notify_type == "face":
                    msg.attach(MIMEText("Система засекла человека!"))
                    telegram_msg = "Система засекла человека! Проверьте почту!"

                if notify_type == "recognize":
                    msg.attach(MIMEText("Система засекла неизвестного человека!"))
                    telegram_msg = "Система засекла неизвестного человека! Проверьте почту!"


                for i, img in enumerate(img_list):
                    filename = "img_tmp.png"
                    cv2.imwrite(filename, img)

                    img_bytes = None

                    with open(filename, 'rb') as f:
                        img_bytes = f.read()

                    os.remove(filename)

                    HEADER = 'Content-Disposition', 'attachment; filename="roi{0}.png"'.format(i)

                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(img_bytes)
                    encoders.encode_base64(attachment)
                    attachment.add_header(*HEADER)
                    msg.attach(attachment)

                self.__server = smtplib.SMTP(HOST, 587)
                self.__server.ehlo()
                self.__server.starttls()
                self.__server.ehlo()
                self.__server.login(self.__config.email, self.__config.password)

                message = msg.as_string()

                self.__server.sendmail(FROM, TO, message)
                self.__server.quit()

            except Exception as ex:
                self._notification_error(f"Failed to notify with email. {ex}")

        if self.__config.notify_telegram:
            try:
                telegram_msg_url = telegram_msg.replace(" ", "%20")
                response = requests.get(rf'https://alarmerbot.ru/?key={self.__config.bot_key}&message={telegram_msg_url}')
            except Exception as ex:
                self._notification_error(f"Failed to notify with Telegram. {ex}")
            pass

    def _notification_info(self, msg: str):
        message = f"[NotificationManager] {msg}"
        logging.info(message)

    def _notification_warn(self, msg: str):
        message = f"[NotificationManager] {msg}"
        logging.warning(message)

    def _notification_error(self, msg: str):
        message = f"[NotificationManager] {msg}"
        logging.error(message)
