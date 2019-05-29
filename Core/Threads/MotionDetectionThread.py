from typing import List, Tuple

import numpy as np

import cv2
import logging
from collections import deque

from PyQt5.QtCore import QThread

from Core import CameraManager
from Core.Data import RoiData
from Core.Utils import ImageOperations as IOps


class MotionDetectionThread(QThread):
    def __init__(self, manager: CameraManager, frames_to_process: int, connect_all_contours = False):
        super().__init__()

        self.__manager: CameraManager = manager
        self.__is_running: bool = False

        self.__scale_factor = 8

        self.__frames_deque: deque = deque()
        self.__frames_to_process: int = frames_to_process
        self.__connect_all_contours = connect_all_contours
        self.__motion_roi: list = []

    def run(self):
        if self.__manager is None:
            self.__motion_thread_warn("Manager is null!")
            return

        self.__is_running = True

        if not self.__prepare_motion_detection():
            self.__motion_thread_warn("Preparation to motion detection is failed!")
            return

        self.__motion_thread_info("Start motion detection")
        IOps.set_kernel_size((40, 40)) #TODO: вынести в настройки

        while self.__is_running:
            motions = self.__detect_motion()

            self.__manager.put_motion_roi(motions)

        self.__motion_thread_info("Motion detection stopped")

    def stop(self):
        self.__is_running = False
        self.__frames_deque.clear()
        self.__motion_thread_info(f"Stopping motion detection")

    def __prepare_motion_detection(self) -> bool:
        try:
            while not len(self.__frames_deque) == self.__frames_to_process:
                img = self.__manager.get_camera_image()
                factor = self.__scale_factor

                height, width = img.shape[:2]

                img_small = cv2.resize(img, (width // factor, height // factor))
                self.__frames_deque.appendleft(img_small)

            self.__motion_thread_info("Preparation to motion detection completed")
            return True

        except Exception as ex:
            self.__motion_thread_error(f"Error during preparation to motion detection {ex}")
            return False

    def __detect_motion(self) -> List[RoiData]:
        """
        Возвращает ROI, где было обнаружено движение
        :return:
        """

        # TODO: если выключена обработка - возвращать весь кадр
        image_data = self.__manager.get_camera_image()

        factor = self.__scale_factor

        height, width = image_data.shape[:2]

        img_small = cv2.resize(image_data, (width // factor, height // factor))

        self.__frames_deque.appendleft(img_small)

        if len(self.__frames_deque) >= self.__frames_to_process:
            self.__motion_roi = []

            try:
                f0 = IOps.ConvertToGray(self.__frames_deque[0])
                f1 = IOps.ConvertToGray(self.__frames_deque[len(self.__frames_deque) // 2])
                f2 = IOps.ConvertToGray(self.__frames_deque[-1])

                movObject = IOps.CreateMovingObject(f0, f1, f2)

                # cv2.imshow("f0", cv2.resize(f0, None, fx=0.2, fy=0.2))
                # cv2.imshow("f1", cv2.resize(f1, None, fx=0.2, fy=0.2))
                # cv2.imshow("f2", cv2.resize(f2, None, fx=0.2, fy=0.2))
                #
                # cv2.imshow("mov_object", movObject)

                # Контуры
                contours = cv2.findContours(np.copy(movObject), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)

                if cv2.__version__[0] != '4':
                    hierarchy = contours[2]
                    contours = contours[1]
                else:
                    hierarchy = contours[1]
                    contours = contours[0]

                contours_big = []

                for cnt in contours:
                    if (cv2.contourArea(cnt) > 0):
                        contours_big.append(cnt)

                if self.__connect_all_contours:
                    roi = IOps.connect_all_contours(contours_big, hierarchy)

                    if roi is not None:
                        x,y,w,h = tuple((x * factor for x in roi))
                        img_roi = image_data[y:x, y + h:x + w]

                        motion_roi = RoiData(img_roi, roi)

                        self.__motion_roi.append(motion_roi)

                else:
                    contours_complete = IOps.ConnectNearbyContours(contours_big, 0)

                    for cnt in contours_big:
                        x,y,w,h = tuple(x * factor for x in cv2.boundingRect(cnt))
                        img_roi = image_data[y:x, y + h:x + w]

                        motion_roi = RoiData(img_roi, (x, y, w, h))

                        self.__motion_roi.append(motion_roi)
            except Exception as ex:
                self.__motion_thread_error(f"{ex}")

            self.__frames_deque.pop()

        return self.__motion_roi

    def __motion_thread_info(self, msg:str):
        message = f"[MotionDetectionThread] {msg}"
        logging.info(message)

    def __motion_thread_warn(self, msg:str):
        message = f"[MotionDetectionThread] {msg}"
        logging.warning(message)

    def __motion_thread_error(self, msg:str):
        message = f"[MotionDetectionThread] {msg}"
        logging.error(message)
