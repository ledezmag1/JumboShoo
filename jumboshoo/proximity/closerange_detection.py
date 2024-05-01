from pathlib import Path
import cv2
from picamera2 import Picamera2
import threading
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
from jumboshoo.utils import print_info_message, print_trace_message, print_warning_message, print_error_message

from jumboshoo.clidisplay import Display
from .classification import classification_list

class CloseProximity:
    def __init__(self, disp: Display, **kwargs):
        model = Path(str(kwargs.get('model_path', 'yolov8n.pt')))
        self.disp_singleton: Display = disp
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = (640,480)
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.preview_configuration.align()
        # picam2.configure("preview")
        self.model=YOLO(model)

        self.camera_on = False

        # self.collecting = False
        # self.collection_thread = threading.Thread(target=self._sample_adc)
        # self.collection_thread.start()

    def start(self):
        print_info_message("Starting picam")

        self.picam2.start()
        self.camera_on = True

    def stop(self):
        print_info_message("Stopping picam")

        self.picam2.stop()
        self.camera_on = False

    def is_elephant(self):
        image = self.picam2.capture_array()
        image = cv2.flip(image,-1)

        results = self.model.predict(image)
        result = results[0]
        # result.show()

        a=results[0].boxes.data
        px=pd.DataFrame(a).astype("float")

        elephant_detected = False

        for index,row in px.iterrows():
            d=int(row[5])
            classification = classification_list[d]
            print_trace_message(f"Class: {classification}")

            if classification == 'elephant':
                elephant_detected = True
                break

        # self.disp_singleton.string1 = "Elephant detected: {}".format(elephant_detected)
        print_info_message("Elephant detected: {}".format(elephant_detected))

        return elephant_detected
        


