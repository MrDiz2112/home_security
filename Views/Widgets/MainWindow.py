# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Views/UI/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1007, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cameraLayout = QtWidgets.QVBoxLayout()
        self.cameraLayout.setObjectName("cameraLayout")
        self.cameraImageLayout = QtWidgets.QVBoxLayout()
        self.cameraImageLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.cameraImageLayout.setObjectName("cameraImageLayout")
        self.cameraImage = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameraImage.sizePolicy().hasHeightForWidth())
        self.cameraImage.setSizePolicy(sizePolicy)
        self.cameraImage.setText("")
        self.cameraImage.setAlignment(QtCore.Qt.AlignCenter)
        self.cameraImage.setObjectName("cameraImage")
        self.cameraImageLayout.addWidget(self.cameraImage)
        self.cameraLayout.addLayout(self.cameraImageLayout)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.cameraLayout.addWidget(self.line_3)
        self.cameraSettingsLayout = QtWidgets.QHBoxLayout()
        self.cameraSettingsLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.cameraSettingsLayout.setObjectName("cameraSettingsLayout")
        self.RoiCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.RoiCheckBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.RoiCheckBox.setObjectName("RoiCheckBox")
        self.cameraSettingsLayout.addWidget(self.RoiCheckBox)
        self.newRoiButton = QtWidgets.QPushButton(self.centralwidget)
        self.newRoiButton.setMinimumSize(QtCore.QSize(180, 0))
        self.newRoiButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.newRoiButton.setObjectName("newRoiButton")
        self.cameraSettingsLayout.addWidget(self.newRoiButton)
        self.editRoiButton = QtWidgets.QPushButton(self.centralwidget)
        self.editRoiButton.setMinimumSize(QtCore.QSize(180, 0))
        self.editRoiButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.editRoiButton.setObjectName("editRoiButton")
        self.cameraSettingsLayout.addWidget(self.editRoiButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.cameraSettingsLayout.addItem(spacerItem)
        self.displayProcessingCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.displayProcessingCheckBox.setEnabled(True)
        self.displayProcessingCheckBox.setChecked(True)
        self.displayProcessingCheckBox.setObjectName("displayProcessingCheckBox")
        self.cameraSettingsLayout.addWidget(self.displayProcessingCheckBox)
        self.cameraLayout.addLayout(self.cameraSettingsLayout)
        self.horizontalLayout.addLayout(self.cameraLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.settingsLayout = QtWidgets.QVBoxLayout()
        self.settingsLayout.setObjectName("settingsLayout")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        self.startButton.setMinimumSize(QtCore.QSize(180, 0))
        self.startButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.startButton.setObjectName("startButton")
        self.settingsLayout.addWidget(self.startButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.settingsLayout.addItem(spacerItem1)
        self.databaseButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.databaseButton.sizePolicy().hasHeightForWidth())
        self.databaseButton.setSizePolicy(sizePolicy)
        self.databaseButton.setMinimumSize(QtCore.QSize(180, 0))
        self.databaseButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.databaseButton.setObjectName("databaseButton")
        self.settingsLayout.addWidget(self.databaseButton)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setMinimumSize(QtCore.QSize(180, 0))
        self.line_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.settingsLayout.addWidget(self.line_2)
        self.notificationButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notificationButton.sizePolicy().hasHeightForWidth())
        self.notificationButton.setSizePolicy(sizePolicy)
        self.notificationButton.setMinimumSize(QtCore.QSize(180, 0))
        self.notificationButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.notificationButton.setObjectName("notificationButton")
        self.settingsLayout.addWidget(self.notificationButton)
        self.notificationCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notificationCheckBox.sizePolicy().hasHeightForWidth())
        self.notificationCheckBox.setSizePolicy(sizePolicy)
        self.notificationCheckBox.setMinimumSize(QtCore.QSize(180, 0))
        self.notificationCheckBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.notificationCheckBox.setObjectName("notificationCheckBox")
        self.settingsLayout.addWidget(self.notificationCheckBox)
        self.horizontalLayout.addLayout(self.settingsLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1007, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Home Security"))
        self.RoiCheckBox.setText(_translate("MainWindow", "Отобразить ROI"))
        self.newRoiButton.setText(_translate("MainWindow", "Новая область"))
        self.editRoiButton.setText(_translate("MainWindow", "Редактировать"))
        self.displayProcessingCheckBox.setText(_translate("MainWindow", "Показать результат обработки"))
        self.startButton.setText(_translate("MainWindow", "Старт"))
        self.databaseButton.setText(_translate("MainWindow", "База лиц"))
        self.notificationButton.setText(_translate("MainWindow", "Настройка оповещений"))
        self.notificationCheckBox.setText(_translate("MainWindow", "Включить оповещения"))

