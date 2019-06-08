import dlib
import numpy as np

from collections import namedtuple
from  typing import Tuple


class RoiData:
    def __init__(self, img: np.ndarray,
                 roi: Tuple[int, int, int, int],
                 shape: dlib.full_object_detection = None,
                 is_motion = True):
        self.img: np.ndarray = img
        self.roi: Tuple[int, int, int, int] = roi
        self.shape: dlib.full_object_detection = shape
        self.is_motion = is_motion
