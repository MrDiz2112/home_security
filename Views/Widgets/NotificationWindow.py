# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Views/UI/NotificationWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_notificationWindow(object):
    def setupUi(self, notificationWindow):
        notificationWindow.setObjectName("notificationWindow")
        notificationWindow.resize(300, 175)
        notificationWindow.setMinimumSize(QtCore.QSize(300, 175))
        notificationWindow.setMaximumSize(QtCore.QSize(400, 175))
        self.verticalLayout = QtWidgets.QVBoxLayout(notificationWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.emailCheckBox = QtWidgets.QCheckBox(notificationWindow)
        self.emailCheckBox.setObjectName("emailCheckBox")
        self.verticalLayout.addWidget(self.emailCheckBox)
        self.emailLineEdit = QtWidgets.QLineEdit(notificationWindow)
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.verticalLayout.addWidget(self.emailLineEdit)
        self.passwordLineEdit = QtWidgets.QLineEdit(notificationWindow)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.verticalLayout.addWidget(self.passwordLineEdit)
        self.telegramCheckBox = QtWidgets.QCheckBox(notificationWindow)
        self.telegramCheckBox.setObjectName("telegramCheckBox")
        self.verticalLayout.addWidget(self.telegramCheckBox)
        self.telegramLineEdit = QtWidgets.QLineEdit(notificationWindow)
        self.telegramLineEdit.setReadOnly(False)
        self.telegramLineEdit.setObjectName("telegramLineEdit")
        self.verticalLayout.addWidget(self.telegramLineEdit)
        self.applyButton = QtWidgets.QPushButton(notificationWindow)
        self.applyButton.setObjectName("applyButton")
        self.verticalLayout.addWidget(self.applyButton)

        self.retranslateUi(notificationWindow)
        QtCore.QMetaObject.connectSlotsByName(notificationWindow)

    def retranslateUi(self, notificationWindow):
        _translate = QtCore.QCoreApplication.translate
        notificationWindow.setWindowTitle(_translate("notificationWindow", "Настройка уведомлений"))
        self.emailCheckBox.setText(_translate("notificationWindow", "Уведомление по e-mail"))
        self.emailLineEdit.setPlaceholderText(_translate("notificationWindow", "Адрес e-mail"))
        self.passwordLineEdit.setPlaceholderText(_translate("notificationWindow", "Пароль"))
        self.telegramCheckBox.setText(_translate("notificationWindow", "Уведомление по Telegram"))
        self.telegramLineEdit.setPlaceholderText(_translate("notificationWindow", "@alarmer_bot key"))
        self.applyButton.setText(_translate("notificationWindow", "Применить"))


