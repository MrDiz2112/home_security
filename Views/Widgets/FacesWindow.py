# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Views/UI/FacesWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_facesWindow(object):
    def setupUi(self, facesWindow):
        facesWindow.setObjectName("facesWindow")
        facesWindow.resize(418, 249)
        self.verticalLayout = QtWidgets.QVBoxLayout(facesWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.facesTable = QtWidgets.QTableWidget(facesWindow)
        self.facesTable.setMinimumSize(QtCore.QSize(400, 200))
        self.facesTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.facesTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.facesTable.setTabKeyNavigation(False)
        self.facesTable.setProperty("showDropIndicator", False)
        self.facesTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.facesTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.facesTable.setTextElideMode(QtCore.Qt.ElideLeft)
        self.facesTable.setShowGrid(False)
        self.facesTable.setCornerButtonEnabled(False)
        self.facesTable.setColumnCount(2)
        self.facesTable.setObjectName("facesTable")
        self.facesTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.facesTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.facesTable.setHorizontalHeaderItem(1, item)
        self.facesTable.horizontalHeader().setVisible(True)
        self.facesTable.horizontalHeader().setCascadingSectionResizes(False)
        self.facesTable.horizontalHeader().setStretchLastSection(True)
        self.facesTable.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.facesTable)
        self.buttounsLayout = QtWidgets.QHBoxLayout()
        self.buttounsLayout.setObjectName("buttounsLayout")
        self.addButton = QtWidgets.QPushButton(facesWindow)
        self.addButton.setObjectName("addButton")
        self.buttounsLayout.addWidget(self.addButton)
        self.deleteButton = QtWidgets.QPushButton(facesWindow)
        self.deleteButton.setObjectName("deleteButton")
        self.buttounsLayout.addWidget(self.deleteButton)
        self.verticalLayout.addLayout(self.buttounsLayout)

        self.retranslateUi(facesWindow)
        QtCore.QMetaObject.connectSlotsByName(facesWindow)

    def retranslateUi(self, facesWindow):
        _translate = QtCore.QCoreApplication.translate
        facesWindow.setWindowTitle(_translate("facesWindow", "База данных лиц"))
        item = self.facesTable.horizontalHeaderItem(0)
        item.setText(_translate("facesWindow", "id"))
        item = self.facesTable.horizontalHeaderItem(1)
        item.setText(_translate("facesWindow", "Имя"))
        self.addButton.setText(_translate("facesWindow", "Добавить"))
        self.deleteButton.setText(_translate("facesWindow", "Удалить"))


