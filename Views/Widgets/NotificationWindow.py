# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/mrdiz/Projects/Python/home_security/Views/UI/NotificationWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_notificationWindow(object):
    def setupUi(self, notificationWindow):
        notificationWindow.setObjectName("notificationWindow")
        notificationWindow.resize(514, 244)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(notificationWindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.emailCheckBox = QtWidgets.QCheckBox(notificationWindow)
        self.emailCheckBox.setObjectName("emailCheckBox")
        self.verticalLayout_2.addWidget(self.emailCheckBox)
        self.emailLineEdit = QtWidgets.QLineEdit(notificationWindow)
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.verticalLayout_2.addWidget(self.emailLineEdit)
        self.smsCheckBox = QtWidgets.QCheckBox(notificationWindow)
        self.smsCheckBox.setObjectName("smsCheckBox")
        self.verticalLayout_2.addWidget(self.smsCheckBox)
        self.lineEdit = QtWidgets.QLineEdit(notificationWindow)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(notificationWindow)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(notificationWindow)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_2.addWidget(self.lineEdit_3)
        self.label = QtWidgets.QLabel(notificationWindow)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.applyButton = QtWidgets.QPushButton(notificationWindow)
        self.applyButton.setObjectName("applyButton")
        self.verticalLayout_2.addWidget(self.applyButton)

        self.retranslateUi(notificationWindow)
        QtCore.QMetaObject.connectSlotsByName(notificationWindow)

    def retranslateUi(self, notificationWindow):
        _translate = QtCore.QCoreApplication.translate
        notificationWindow.setWindowTitle(_translate("notificationWindow", "Настройка уведомлений"))
        self.emailCheckBox.setText(_translate("notificationWindow", "Уведомление по e-mail"))
        self.smsCheckBox.setText(_translate("notificationWindow", "Уведомление по SMS"))
        self.label.setText(_translate("notificationWindow", "Настроить аккаунт Twilio"))
        self.applyButton.setText(_translate("notificationWindow", "Применить"))


