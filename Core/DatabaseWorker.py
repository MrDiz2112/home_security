import os
import sqlite3

import cv2
import dlib
import numpy as np

from Core.Config import ResourcesConfig


class DatabaseWorker:
    def __init__(self):
        self.__id = 'id'
        self.__name = 'name'
        self.__face = 'face'
        self.__desc = 'desc'

        self.__db_name = 'faces.sqlite'
        self.__table = 'faces'

        pass

    def create_db(self):
        con = sqlite3.connect(self.__db_name)
        cursor = con.cursor()

        sql = f'''
        CREATE TABLE IF NOT EXISTS {self.__table}
        (
            {self.__id} INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
            {self.__name} TEXT NOT NULL,
            {self.__face} BLOB NOT NULL,
            {self.__desc} TEXT NOT NULL 
        )'''

        cursor.execute(sql)
        con.close()

    def select_all_faces(self):
        con = sqlite3.connect(self.__db_name)
        cursor = con.cursor()

        sql = f'''SELECT * FROM {self.__table}'''

        cursor.execute(sql)

        values = cursor.fetchall()
        con.close()

        return values

    def insert_face(self, name: str, img: np.ndarray):
        config = ResourcesConfig()

        sp = dlib.shape_predictor(config.shape_predictor)
        facerec = dlib.face_recognition_model_v1(config.recognition_resnet)
        detector = dlib.get_frontal_face_detector()

        b, g, r = cv2.split(img)
        img_rgb = cv2.merge((r, g, b))

        desc = None

        dets = detector(img_rgb, 1)
        for k, d in enumerate(dets):
            shape = sp(img_rgb, d)
            desc = facerec.compute_face_descriptor(img_rgb, shape)

        face_bytes = img.tobytes()
        desc_bytes = str(desc)

        con = sqlite3.connect(self.__db_name)
        cursor = con.cursor()

        sql = f"""
        INSERT INTO {self.__table}({self.__name}, {self.__face}, {self.__desc})
        VALUES (?, ?, ?)
        """

        cursor.execute(sql, (name, face_bytes, desc_bytes))

        con.commit()
        con.close()

    def delete_face(self, id: int):
        con = sqlite3.connect(self.__db_name)
        cursor = con.cursor()

        sql = f"DELETE FROM {self.__table} WHERE {self.__id} = {id}"

        cursor.execute(sql)
        con.commit()
        con.close()
