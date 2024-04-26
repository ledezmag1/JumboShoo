from pathlib import Path
import cv2
from picamera2 import Picamera2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np

class LongProximity:
    def __init__(self, **kwargs):
        model = Path(kwargs.get('model_path'))
        picam2 = Picamera2()
        picam2.preview_configuration.main.size = (640,480)
        picam2.preview_configuration.main.format = "RGB888"
        picam2.preview_configuration.align()
        picam2.configure("preview")
        picam2.start()
        model=YOLO('yolov8n.pt')
        my_file = open("coco.txt", "r")
        data = my_file.read()

        

        pass
