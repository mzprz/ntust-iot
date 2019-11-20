import json
import paho.mqtt.client as mqtt
import numpy as np
import time as tm
from datetime import datetime
import time
import cv2

from tensorflow.keras import Input, Model
from darknet import darknet_base
from predict import predict, predict_with_yolo_head


INCLUDE_YOLO_HEAD = True

stream = cv2.VideoCapture(1)

inputs = Input(shape=(None, None, 3))
outputs, config = darknet_base(inputs, include_yolo_head=False)
model = Model(inputs, outputs)


# ===========================================================
# FUNCTIONS DECLARATION
# ===========================================================

# Function to Init Status


def initStatus():
    for area in range(len(last_status)):
        payload = {
            'area': area + 1,
            'status': last_status[area]
        }
        payload_json = json.dumps(payload)
        client.publish('dataAlert', payload_json)
    print("Init Success")

# ===========================================================
# MAIN PROGRAM
# ===========================================================

# 1. INIT


# a. Init MQTT
client = mqtt.Client("Camera")
client.connect(
    host='192.168.43.242',
    port=1884
)

# b. Init Status
last_status = [0, 0, 0, 0]
initStatus()

# -----------------------------------------------------------

# 2. LOOP
while True:

    # Capture frame-by-frame
    grabbed, frame = stream.read()
    if not grabbed:
        break

    # Run detection
    start = time.time()
    output_image, is_inside = predict_with_yolo_head(model, frame, config, confidence=0.3, iou_threshold=0.4)

    # output_image = frame
    end = time.time()
    print("Inference time: {:.2f}s".format(end - start))
    
    # Display the resulting frame
    cv2.imshow('', output_image)

    # Data hasil image processing
    print(is_inside)
    status = 1 if is_inside else 0
    area = 1

    # Data Tambahan
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time_now = now.strftime("%H:%M:%S")
    filename = now.strftime("%d%m-%H:%M") + '(' + str(area) + ').mp4'

    # Membuat format payload
    payload = {
        'date': date,
        'time': time_now,
        'area': area,
        'filename': filename,
        'status': status
    }
    payload_json = json.dumps(payload)

    # Mengirim data hanya saat ada perubahan status
    if last_status[area - 1] != status:
        print(payload_json)
        client.publish('dataAlert', payload_json)
        last_status[area - 1] = status

    # Delay
    tm.sleep(1)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# -----------------------------------------------------------
