import logging
import os
import threading
import time
from collections import deque
from queue import Queue
from threading import Thread
from typing import List, Callable

import cv2
import dlib
import numpy as np

from Core.Config import ResourcesConfig, ProcessingConfig
from Core.Data import RoiData
from Core.Threads import RecognitionThread
from Core.Utils import ImageOperations as IOps


class FrameProcessing:
    def __init__(self, name: str, get_actual_frame: Callable[[] , np.ndarray]):
        super().__init__()

        self.__config = ProcessingConfig()

        # Notification
        from Core import NotificationManager
        self.__notification_manager = NotificationManager()
        self.__notify_thread = None
        self.__notify_thread_started = False
        self.__new_roi_delay = 3  # seconds
        self.__actual_frame = None

        self.__name = name
        self.__get_actual_frame = get_actual_frame
        self.__roi_list: List[RoiData] = []
        self.__notify_roi = []

        # Motion
        self.__frames_deque: deque = deque()
        self.__motion_scale_factor = 8
        self.__frames_to_process = 7
        self.__connect_all_contours = False
        self.__motion_roi = []

        self.__resources_config = ResourcesConfig()

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
        threading.current_thread().name = "ProcessingThread"

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
            sp_path = self.__resources_config.shape_predictor

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
            fr_path = self.__resources_config.recognition_resnet

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

        if motions and not self.__config.detect_faces \
                and not self.__config.recognize_faces \
                and self.__config.detect_motion:
            self.__start_notify_thread("motion")


        for motion_roi in motions:
            if self.__config.display_result:
                self.__roi_list.append(motion_roi)

            faces = self.__detect_face(motion_roi)

            for face_roi in faces:
                if self.__config.display_result:
                    self.__roi_list.append(face_roi)

                    if not self.__config.recognize_faces and self.__config.detect_faces:
                        self.__notify_roi.append(face_roi.img[:])
                        self.__start_notify_thread("face")

                self.__faces.put(face_roi)

    def __detect_motion(self) -> List[RoiData]:
        """
        Возвращает ROI, где было обнаружено движение
        :return:
        """

        self.__motion_roi = []

        # TODO: если выключена обработка - возвращать весь кадр
        image_data = self.__get_actual_frame()

        if image_data is None:
            return []

        self.__actual_frame = image_data[:]

        if not self.__config.detect_motion:
            x, y, w, h = (0,0, image_data.shape[1], image_data.shape[0])
            img_roi = image_data[y:y + h, x:x + w]

            motion_roi = RoiData(img_roi, (x, y, w, h))

            self.__motion_roi.append(motion_roi)
            return self.__motion_roi

        factor = self.__motion_scale_factor

        height, width = image_data.shape[:2]

        img_small = cv2.resize(image_data, (width // factor, height // factor))

        self.__frames_deque.appendleft(img_small)

        if len(self.__frames_deque) >= self.__frames_to_process:

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

        if not self.__config.detect_faces:
            self.__faces_roi.append(motion_roi)
            return self.__faces_roi

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

                x_offset = x // factor
                y_offset = y // factor


                img_roi = img_small[:]

                face_roi = RoiData(img_roi, ((x_offset + roi.left()) * factor,
                                             (y_offset + roi.top()) * factor,
                                             (roi.right() - roi.left()) * factor,
                                             (roi.bottom() - roi.top()) * factor),
                                   shape, False)

                # img_roi = img[(roi.top() * factor):(roi.bottom() * factor),
                #           (roi.left() * factor):(roi.right() * factor)]
                #
                # win = dlib.image_window()
                # win.clear_overlay()
                # win.set_image(img_roi)
                # win.add_overlay(shape)
                # win.wait_until_closed()
                #
                # face_roi = RoiData(img_roi, (x_offset + (roi.left() * factor),
                #                              y_offset + (roi.top() * factor),
                #                              (roi.right() * factor) - (roi.left() * factor),
                #                              (roi.bottom() * factor) - (roi.top() * factor)),
                #                    shape, False)

                # cv2.imshow("face", img_roi)
                # cv2.waitKey(1)

                self.__faces_roi.append(face_roi)
        except Exception as ex:
            self.__processing_error(f"{ex}")

        return self.__faces_roi

    def __start_notify_thread(self, notify_type: str):
        if not self.__notify_thread_started:
            self.__notify_thread_started = True
            self.__notify_thread = Thread(target=self.__send_notification, args=(notify_type,))
            self.__notify_thread.name = "NotificationThread"
            self.__notify_thread.start()

    def __send_notification(self, notify_type: str):
        try:
            if notify_type == 'motion':
                while len(self.__notify_roi) < 5:
                    self.__notify_roi.append(self.__actual_frame)
                    time.sleep(self.__new_roi_delay)
            else:
                while True:
                    if len(self.__notify_roi) >= 5:
                        break

                    before_sleep_len = len(self.__notify_roi)

                    time.sleep(self.__new_roi_delay)

                    if len(self.__notify_roi) == before_sleep_len:
                        break

            self.__notification_manager.send_notifications(notify_type, self.__notify_roi[:])
        except Exception as ex:
            self.__processing_error(f"Failed to send notification! {ex}")

        self.__notify_roi = []
        self.__notify_thread_started = False

    def __processing_info(self, msg:str):
        message = f"[FrameProcessing {self.__name}] {msg}"
        logging.info(message)

    def __processing_warn(self, msg:str):
        message = f"[FrameProcessing {self.__name}] {msg}"
        logging.warning(message)

    def __processing_error(self, msg:str):
        message = f"[FrameProcessing {self.__name}] {msg}"
        logging.error(message)
