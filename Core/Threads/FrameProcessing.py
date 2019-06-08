import logging
import os
from collections import deque
from queue import Queue
from threading import Thread
from typing import List, Callable

import cv2
import dlib
import numpy as np

from Core.Data import RoiData
from Core.Threads import RecognitionThread
from Core.Utils import ImageOperations as IOps


class FrameProcessing:
    def __init__(self, name: str, get_actual_frame: Callable[[] , np.ndarray]):
        super().__init__()

        self.__name = name
        self.__get_actual_frame = get_actual_frame
        self.__roi_list: List[RoiData] = []

        # Motion
        self.__frames_deque: deque = deque()
        self.__motion_scale_factor = 8
        self.__frames_to_process = 10
        self.__connect_all_contours = False
        self.__motion_roi = []

        # Face
        self.__faces_roi = []
        self.__shape_predictor = None
        self.__detector = dlib.get_frontal_face_detector()
        self.__face_scale_factor = 2

        # Recognition
        self.__face_rec_model: dlib.face_recognition_model_v1 = None
        self.__faces: Queue = Queue()

        self.__is_running = False
        self.__processing_thread = None
        self.__recognition_thread = None

    def get_roi_list(self) -> List[RoiData]:
        return self.__roi_list

    def __start_processing(self):
        while self.__is_running:
            self.__process()

    def start(self):
        self.__is_running = True
        self.__processing_info("Prepare frame processing")

        self.__prepare_motion_detection()
        self.__prepare_face_detection()
        self.__prepare_recognition()

        self.__processing_info("Preparation to frame processing finished")

        self.__recognition_thread = RecognitionThread(self.__faces, self.__face_rec_model)
        self.__recognition_thread.start()

        self.__processing_thread = Thread(target=self.__start_processing)
        self.__processing_thread.name = f"FrameProcessing[{self.__name}]"
        self.__processing_thread.start()

    def stop(self):
        self.__is_running = False
        self.__recognition_thread.stop()

    def __prepare_motion_detection(self) -> bool:
        try:
            while not len(self.__frames_deque) == self.__frames_to_process:
                img = self.__get_actual_frame()

                if img is None:
                    continue

                factor = self.__motion_scale_factor

                height, width = img.shape[:2]

                img_small = cv2.resize(img, (width // factor, height // factor))
                self.__frames_deque.appendleft(img_small)

            self.__processing_info("Preparation to motion detection completed")
            return True

        except Exception as ex:
            self.__processing_error(f"Error during preparation to motion detection {ex}")
            return False

    def __prepare_face_detection(self) -> bool:
        try:
            sp_path = os.path.join(os.getcwd(), "Resources", "face_shape_predictor.dat")

            if not os.path.exists(sp_path):
                self.__processing_warn("Missing resource .dat files")
                return False

            self.__shape_predictor = dlib.shape_predictor(sp_path)

            self.__processing_info("Preparation to motion detection completed")
            return True

        except Exception as ex:
            self.__processing_error(f"Error during preparation to face detection {ex}")
            return False

    def __prepare_recognition(self) -> bool:
        try:
            fr_path = os.path.join(os.getcwd(), "Resources", "face_recognition_resnet.dat")

            if not os.path.exists(fr_path):
                self.__processing_warn("Missing resource .dat files")
                return False

            self.__face_rec_model = dlib.face_recognition_model_v1(fr_path)

            self.__processing_info("Preparation to recognition completed")
            return True

        except Exception as ex:
            self.__processing_error(f"Error during preparation to recognition {ex}")
            return False

    def __process(self):
        motions = self.__detect_motion()

        for motion_roi in motions:

            self.__roi_list.append(motion_roi)
            faces = self.__detect_face(motion_roi)

            for face_roi in faces:
                self.__roi_list.append(face_roi)
                self.__faces.put(face_roi)

    def __detect_motion(self) -> List[RoiData]:
        """
        Возвращает ROI, где было обнаружено движение
        :return:
        """

        # TODO: если выключена обработка - возвращать весь кадр
        image_data = self.__get_actual_frame()

        if image_data is None:
            return []

        factor = self.__motion_scale_factor

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
                        img_roi = image_data[y:y + h, x:x + w]

                        motion_roi = RoiData(img_roi, (x, y, w, h))

                        self.__motion_roi.append(motion_roi)
            except Exception as ex:
                self.__processing_error(f"{ex}")

            self.__frames_deque.pop()

        return self.__motion_roi

    def __detect_face(self, motion_roi: RoiData) -> List[RoiData]:
        """
        Возвращает ROI, где было обнаружено лицо
        :return:
        """
        self.__faces_roi = []
        try:
            # TODO: если выключена обработка - возвращать весь кадр

            x = motion_roi.roi[0]
            y = motion_roi.roi[1]
            w = motion_roi.roi[2]
            h = motion_roi.roi[3]

            factor = self.__face_scale_factor

            img: np.ndarray = motion_roi.img

            img_small = cv2.resize(img, (w // factor, h // factor))

            b,g,r = cv2.split(img_small)
            img_rgb = cv2.merge((r,g,b))

            dets = self.__detector(img_rgb, 1)

            #TODO: расчитать смещение roi

            for k, d in enumerate(dets):
                shape : dlib.full_object_detection = self.__shape_predictor(img_rgb, d)
                roi: dlib.rectangle = shape.rect

                x_offset = x
                y_offset = y

                img_roi = img[(roi.top() * factor):(roi.bottom() * factor),
                          (roi.left() * factor):(roi.right() * factor)]

                face_roi = RoiData(img_roi, (x_offset + (roi.left() * factor),
                                             y_offset + (roi.top() * factor),
                                             (roi.right() * factor) - (roi.left() * factor),
                                             (roi.bottom() * factor) - (roi.top() * factor)),
                                   shape, False)

                cv2.imshow("face", img_roi)
                cv2.waitKey(1)

                self.__faces_roi.append(face_roi)
        except Exception as ex:
            self.__processing_error(f"{ex}")

        return self.__faces_roi

    def __processing_info(self, msg:str):
        message = f"[FrameProcessing {self.__name}] {msg}"
        logging.info(message)

    def __processing_warn(self, msg:str):
        message = f"[FrameProcessing {self.__name}] {msg}"
        logging.warning(message)

    def __processing_error(self, msg:str):
        message = f"[FrameProcessing {self.__name}] {msg}"
        logging.error(message)
