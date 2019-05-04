from typing import List, Tuple

import numpy as np

import cv2
import logging
from collections import deque

from PyQt5.QtCore import QThread

from Core import Manager
from Core.Utils import ImageOperations as IOps


class MotionDetectionThread(QThread):
    def __init__(self, manager: Manager, frames_to_process: int):
        super().__init__()

        self.__manager: Manager = manager
        self.__is_running: bool = False

        self.__frames_deque: deque = deque()
        self.__frames_to_process: int = frames_to_process
        self.motion_roi: list = []

    def run(self):
        if self.__manager is None:
            self.__motion_thread_warn("Manager is null!")
            return

        self.__is_running = True

        if not self.__prepare_motion_detection():
            self.__motion_thread_warn("Preparation to motion detection is failed!")
            return

    def __prepare_motion_detection(self) -> bool:
        try:
            while not self.__frames_deque.count == self.__frames_to_process:
                img = self.__manager.get_camera_image()
                self.__frames_deque.appendleft(img)

            self.__motion_thread_info("Preparation completed")
            return True

        except Exception as ex:
            self.__motion_thread_error(f"Error during preparation {ex}")
            return False

    # TODO: возвращать ROI с координатами движения
    def __detect_motion(self, image_data: np.ndarray) -> List[Tuple[int, int, int, int]]:

        self.frames_deque.appendleft(image_data)

        if len(self.frames_deque) >= self.__frames_to_process:
            self.motion_roi = []

            f0 = IOps.ConvertToGray(self.frames_deque[0])
            f1 = IOps.ConvertToGray(self.frames_deque[len(self.frames_deque) // 2])
            f2 = IOps.ConvertToGray(self.frames_deque[-1])

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
                contours = contours[1]
            else:
                contours = contours[0]

            contours_big = []

            for cnt in contours:
                if cv2.contourArea(cnt) > 70:
                    contours_big.append(cnt)

            contours_complete = IOps.ConnectNearbyContours(contours_big, 70)

            for cnt in contours_complete:
                # self.DrawRectangle(cnt, self.frame_to_draw)
                self.motion_roi.append(cv2.boundingRect(cnt))

            self.frames_deque.pop()

        return self.motion_roi

    # TODO: нет ссылок
    def __draw_rectangle(self, cnt, img):
        x, y, w, h = cv2.boundingRect(cnt)

        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(img, (cx, cy), 3, (255, 255, 0), 3)

    def __motion_thread_info(self, msg:str):
        message = f"[MotionDetectionThread] {msg}"
        logging.info(message)

    def __motion_thread_warn(self, msg:str):
        message = f"[MotionDetectionThread] {msg}"
        logging.warning(message)

    def __motion_thread_error(self, msg:str):
        message = f"[MotionDetectionThread] {msg}"
        logging.error(message)
