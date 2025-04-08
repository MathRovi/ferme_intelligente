import requests
import msgpack
import base64
from datetime import datetime
import time
import random

# ✅ URL correcte de l'API
url = "http://localhost:8000/api/v1/receive"

# ✅ Active cette variable pour tester des anomalies
FORCE_ANOMALIES = True

while True:
    if FORCE_ANOMALIES:
        temperature = round(random.uniform(41.0, 45.0), 2)  # Température anormale
        humidity = round(random.uniform(5.0, 19.9), 2)       # Humidité anormale
    else:
        temperature = round(random.uniform(18.0, 30.0), 2)
        humidity = round(random.uniform(30.0, 90.0), 2)

    payload = {
        "sensor_id": random.randint(1, 6),
        "plant_id": random.randint(1, 6),
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": temperature,
        "humidity": humidity,
        "version": "FR-v8"
    }

    packed = msgpack.packb(payload)
    encoded = base64.b64encode(packed)

    try:
        response = requests.post(url, data=encoded)
        print(f"[SEND] {payload} → {response.status_code} | {response.json()}")
    except Exception as e:
        print(f"[ERROR] {e}")

    time.sleep(2)
