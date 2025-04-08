# simulate_loop.py

import requests
import msgpack
import base64
from datetime import datetime
import time
import random

url = "http://localhost:8000/api/v1/receive"
FORCE_ANOMALIES = True
NUM_CAPTEURS = 6
TEMPS_PAR_CAPTEUR = 2

global_cycle_id = 85

while True:
    for i in range(1, NUM_CAPTEURS + 1):
        if FORCE_ANOMALIES and i % 3 == 0:
            temperature = round(random.uniform(41.0, 45.0), 2)
            humidity = round(random.uniform(5.0, 19.9), 2)
        else:
            temperature = round(random.uniform(18.0, 30.0), 2)
            humidity = round(random.uniform(30.0, 90.0), 2)

        payload = {
            "sensor_id": i,
            "plant_id": i,
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": temperature,
            "humidity": humidity,
            "version": "FR-v8",
            "cycle_id": global_cycle_id  # ✅ Ajout ici
        }

        packed = msgpack.packb(payload)
        encoded = base64.b64encode(packed)

        try:
            response = requests.post(url, data=encoded)
            print(f"[SEND CYCLE {global_cycle_id}] capteur {i} → {response.status_code} | {response.json()}")
        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(TEMPS_PAR_CAPTEUR)

    global_cycle_id += 1
