import json
import paho.mqtt.client as mqtt
import numpy as np
from datetime import datetime
import time as tm
# datetime object containing current date and time


# some variables
last_status = [0,0,0,0]
client = mqtt.Client("Camera")
client.connect(
    host='localhost',
    port=1884
)

# LOOP
while True:
    status = np.random.randint(0, high=2)
    area = np.random.randint(1, high=5)

    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M:%S")
    filename = now.strftime("%d%m-%H:%M") + '(' + str(area) + ').mp4'

    payload = {
        'date': date,
        'time': time,
        'area': area,
        'filename': filename,
        'status': status
    }

    payload_json = json.dumps(payload)


    if last_status[area-1] != status:
        print(payload_json)
        client.publish('dataAlert', payload_json)
        last_status[area-1] = status
    tm.sleep(1)
