import numpy as np

from collections import namedtuple
from  typing import Tuple


class MotionRoi:
    def __init__(self, img: np.ndarray, roi: Tuple[int, int, int, int]):
        self.img: np.ndarray = img
        self.roi: Tuple[int, int, int, int] = roi