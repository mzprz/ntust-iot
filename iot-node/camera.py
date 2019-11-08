import json
import paho.mqtt.client as mqtt
import numpy as np
from datetime import datetime
# datetime object containing current date and time


# some variables
last_status = 0

# LOOP
status = 1

if last_status != status:
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M:%S")
    area = np.random.randint(1, high=5)
    filename = now.strftime("%d%m-%H:%M") + '(' + str(area) + ').mp4'

    payload = {
        'date': date,
        'time': time,
        'area': area,
        'filename': filename,
        'status': status
    }

    payload_json = json.dumps(payload)

    # MQTT STUFF
    client = mqtt.Client("Camera")
    client.connect(
        host='localhost',
        port=1884
    )
    client.publish('dataAlert', payload_json)
    print(payload_json)
    last_status = status
