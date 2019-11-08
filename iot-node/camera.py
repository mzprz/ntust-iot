import json
import paho.mqtt.client as mqtt
import numpy as np
import time as tm
from datetime import datetime

# INIT
last_status = [0,0,0,0]
client = mqtt.Client("Camera")
client.connect(
    host='localhost',
    port=1884
)

# LOOP
while True:
    # Data hasil image processing
    status = np.random.randint(0, high=2)
    area = np.random.randint(1, high=5)

    # Data Tambahan
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M:%S")
    filename = now.strftime("%d%m-%H:%M") + '(' + str(area) + ').mp4'

    # Membuat format payload
    payload = {
        'date': date,
        'time': time,
        'area': area,
        'filename': filename,
        'status': status
    }
    payload_json = json.dumps(payload)

    # Mengirim data hanya saat ada perubahan status
    if last_status[area-1] != status:
        print(payload_json)
        client.publish('dataAlert', payload_json)
        last_status[area-1] = status

    # Delay
    tm.sleep(1)
