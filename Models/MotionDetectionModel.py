import sys
from typing import List, Tuple
from collections import deque

import cv2

from Models.ImageOperations import ImageOperations as IOps

import numpy as np

# TODO: выбор метода детекции движения
class MotionDetectionModel:
    def __init__(self, frames_distance: int = 5):
        self.frames_deque = deque()
        self.frames_distance = frames_distance
        self.frames_to_process = 3
        self.motion_roi = []

        self.frames_count = 0

    # TODO: возвращать ROI с координатами движения
    def detect_motion(self, image_data: np.ndarray) -> List[Tuple[int, int, int, int]]:
        if len(self.frames_deque) < self.frames_to_process:
            self.frames_count += 1

            if self.frames_count % self.frames_distance == 0:
                self.frames_deque.append(image_data)
                self.frames_count = 0
        else:
            self.motion_roi = []

            f0 = IOps.ConvertToGray(self.frames_deque[0])
            f1 = IOps.ConvertToGray(self.frames_deque[1])
            f2 = IOps.ConvertToGray(self.frames_deque[2])

            movObject = IOps.CreateMovingObject(f0, f1, f2)

            # Контуры
            contours, hierarchy = cv2.findContours(np.copy(movObject),
                                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            contours_big = []

            for cnt in contours:
                if (cv2.contourArea(cnt) > 70):
                    contours_big.append(cnt)

            contours_complete = IOps.ConnectNearbyContours(contours_big, 70)

            for cnt in contours_complete:
                # self.DrawRectangle(cnt, self.frame_to_draw)
                self.motion_roi.append(cv2.boundingRect(cnt))

            self.frames_deque.popleft()

        return self.motion_roi

    def DrawRectangle(self, cnt, img):
        x, y, w, h = cv2.boundingRect(cnt)

        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(img, (cx, cy), 3, (255, 255, 0), 3)
