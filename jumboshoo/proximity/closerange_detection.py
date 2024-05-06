from pathlib import Path
import cv2
from picamera2 import Picamera2
import threading
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np
from jumboshoo.utils import print_info_message, print_warning_message, print_error_message, print_context_message

from jumboshoo.clidisplay import Display
from .classification import classification_list

class CloseProximity:
    def __init__(self, **kwargs):
        print_context_message("Initializing Close Proximity (picam + nn classifier)")
        model = Path(str(kwargs.get('model_path', 'yolov8n.pt')))
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = (640,480)
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.preview_configuration.align()
        # picam2.configure("preview")
        print_info_message(f"Loading {model.name} from {model}")
        self.model=YOLO(model)

        self.camera_on = False

    def start(self):
        print_info_message("Starting picam")

        self.picam2.start()
        self.camera_on = True

    def stop(self):
        print_info_message("Stopping picam")

        self.picam2.stop()
        self.camera_on = False

    def is_elephant(self) -> bool:
        image = self.picam2.capture_array()
        image = cv2.flip(image,-1)

        results = self.model.predict(image, verbose=False)
        result = results[0]

        a=results[0].boxes.data
        px=pd.DataFrame(a).astype("float")

        elephant_detected = False

        for index,row in px.iterrows():
            d=int(row[5])
            classification = classification_list[d]

            if classification == 'elephant':
                elephant_detected = True
                break

        return elephant_detected
        
