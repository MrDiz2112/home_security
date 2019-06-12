# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Views/UI/ProcessingWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_processingWindow(object):
    def setupUi(self, processingWindow):
        processingWindow.setObjectName("processingWindow")
        processingWindow.resize(220, 150)
        processingWindow.setMinimumSize(QtCore.QSize(220, 150))
        processingWindow.setMaximumSize(QtCore.QSize(220, 150))
        self.verticalLayout = QtWidgets.QVBoxLayout(processingWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.motionCheckBox = QtWidgets.QCheckBox(processingWindow)
        self.motionCheckBox.setChecked(True)
        self.motionCheckBox.setObjectName("motionCheckBox")
        self.verticalLayout.addWidget(self.motionCheckBox)
        self.faceCheckBox = QtWidgets.QCheckBox(processingWindow)
        self.faceCheckBox.setChecked(True)
        self.faceCheckBox.setObjectName("faceCheckBox")
        self.verticalLayout.addWidget(self.faceCheckBox)
        self.recognitionCheckBox = QtWidgets.QCheckBox(processingWindow)
        self.recognitionCheckBox.setChecked(True)
        self.recognitionCheckBox.setObjectName("recognitionCheckBox")
        self.verticalLayout.addWidget(self.recognitionCheckBox)
        self.displayProcessingCheckBox = QtWidgets.QCheckBox(processingWindow)
        self.displayProcessingCheckBox.setEnabled(True)
        self.displayProcessingCheckBox.setChecked(True)
        self.displayProcessingCheckBox.setObjectName("displayProcessingCheckBox")
        self.verticalLayout.addWidget(self.displayProcessingCheckBox)
        self.applyButton = QtWidgets.QPushButton(processingWindow)
        self.applyButton.setObjectName("applyButton")
        self.verticalLayout.addWidget(self.applyButton)

        self.retranslateUi(processingWindow)
        QtCore.QMetaObject.connectSlotsByName(processingWindow)

    def retranslateUi(self, processingWindow):
        _translate = QtCore.QCoreApplication.translate
        processingWindow.setWindowTitle(_translate("processingWindow", "Настройка обработки"))
        self.motionCheckBox.setText(_translate("processingWindow", "Включить обнаружения движения"))
        self.faceCheckBox.setText(_translate("processingWindow", "Включить поиск лиц"))
        self.recognitionCheckBox.setText(_translate("processingWindow", "Включить распознавание лиц"))
        self.displayProcessingCheckBox.setText(_translate("processingWindow", "Показать результат обработки"))
        self.applyButton.setText(_translate("processingWindow", "Применить"))


