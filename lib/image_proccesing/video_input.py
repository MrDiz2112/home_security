import cv2 as cv
import numpy as np


class VideoInput:
    def __init__(self, **options):
        self.video = options.get("video")
        self.cam_id = options.get("cam_id")
        self.url = options.get("url")

        if self.video is not None:
            self._cam = cv.VideoCapture(self.video)

        if self.cam_id is not None:
            self._cam = cv.VideoCapture(self.cam_id)

        if self.cam_id is not None:
            self._cam = cv.VideoCapture(self.url)