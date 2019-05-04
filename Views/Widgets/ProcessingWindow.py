# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/mrdiz/Projects/Python/home_security/Views/UI/ProcessingWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(255, 113)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.motionCheckBox = QtWidgets.QCheckBox(Form)
        self.motionCheckBox.setChecked(True)
        self.motionCheckBox.setObjectName("motionCheckBox")
        self.verticalLayout.addWidget(self.motionCheckBox)
        self.faceDetectioncheckBox = QtWidgets.QCheckBox(Form)
        self.faceDetectioncheckBox.setChecked(True)
        self.faceDetectioncheckBox.setObjectName("faceDetectioncheckBox")
        self.verticalLayout.addWidget(self.faceDetectioncheckBox)
        self.recognitionCheckBox = QtWidgets.QCheckBox(Form)
        self.recognitionCheckBox.setChecked(True)
        self.recognitionCheckBox.setObjectName("recognitionCheckBox")
        self.verticalLayout.addWidget(self.recognitionCheckBox)
        self.applyButton = QtWidgets.QPushButton(Form)
        self.applyButton.setObjectName("applyButton")
        self.verticalLayout.addWidget(self.applyButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Настройка обработки"))
        self.motionCheckBox.setText(_translate("Form", "Включить обнаружения движения"))
        self.faceDetectioncheckBox.setText(_translate("Form", "Включить поиск лиц"))
        self.recognitionCheckBox.setText(_translate("Form", "Включить распознавание лиц"))
        self.applyButton.setText(_translate("Form", "Применить"))


