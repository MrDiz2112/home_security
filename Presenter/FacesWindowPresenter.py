import logging

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QTableWidget, QTableWidgetItem

from Core import DatabaseWorker

class FacesWindowPresenter:
    def __init__(self, view):
        self.__view = view

    def add_face(self):
        try:
            file = QFileDialog.getOpenFileName(self.__view, 'Выберите изображение с лицом')

            name, ok = QInputDialog.getText(self.__view, 'Добавление нового лица', 'Введите имя')

            img = cv2.imread(file[0])

            db_worker = DatabaseWorker()

            db_worker.insert_face(name, img)

            self.fill_table()
        except Exception as ex:
            self.__presenter_error(f"Cannot add face to database. {ex}")

    def delete_face(self):
        table: QTableWidget = self.__view.facesTable

        items = table.selectedItems()

        if items:
            id = int(items[0].text())

            db_worker = DatabaseWorker()

            db_worker.delete_face(id)
            self.fill_table()

    def fill_table(self):
        try:
            db_worker = DatabaseWorker()

            values = db_worker.select_all_faces()

            table: QTableWidget = self.__view.facesTable

            table.setRowCount(len(values))

            for i, face_item in enumerate(values):
                id_item = QTableWidgetItem(str(face_item[0]))
                name_item = QTableWidgetItem(face_item[1])

                id_item.setTextAlignment(Qt.AlignCenter)
                name_item.setTextAlignment(Qt.AlignCenter)

                table.setItem(i, 0, id_item)
                table.setItem(i, 1, name_item)
        except Exception as ex:
            self.__presenter_error(f"Cannot display table. {ex}")

    def __presenter_info(self, msg: str):
        message = f"[FacesWindowPresenter] {msg}"
        logging.info(message)

    def __presenter_warn(self, msg: str):
        message = f"[FacesWindowPresenter] {msg}"
        logging.warning(message)

    def __presenter_error(self, msg: str):
        message = f"[FacesWindowPresenter] {msg}"
        logging.error(message)


