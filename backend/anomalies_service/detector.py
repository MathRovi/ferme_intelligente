def detect_anomalies(measurements):
    anomalies = []
    for m in measurements:
        if m["temperature"] > 40 or m["humidity"] < 20:
            anomalies.append({
                "sensor_id": m["sensor_id"],
                "timestamp": m["timestamp"],
                "type": "Valeur hors plage",
                "details": f"Temp={m['temperature']}, Hum={m['humidity']}",
                "severity": "warning"
            })
    return anomalies
