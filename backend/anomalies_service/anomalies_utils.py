# anomalies_service/anomalies_utils.py

import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Chargement de l’environnement
load_dotenv(dotenv_path="config.env")

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "ferme"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432)
    )

def get_recent_measurements():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, sensor_id, temperature, humidity FROM measurements ORDER BY timestamp DESC LIMIT 100")
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "sensor_id": r[1],
            "temperature": r[2],
            "humidity": r[3]
        }
        for r in rows
    ]

def detect_anomalies(measurements):
    anomalies = []
    for m in measurements:
        if m["temperature"] > 40 or m["humidity"] < 20:
            anomalies.append({
                "sensor_id": m["sensor_id"],
                "timestamp": datetime.utcnow(),
                "type": "Valeur hors plage",
                "details": f"Temp={m['temperature']}, Hum={m['humidity']}",
                "severity": "warning"
            })
    return anomalies

def insert_anomalies(anomalies):
    conn = get_db_connection()
    cur = conn.cursor()
    for a in anomalies:
        cur.execute(
            "INSERT INTO anomalies (sensor_id, timestamp, type, details, severity) VALUES (%s, %s, %s, %s, %s)",
            (a["sensor_id"], a["timestamp"], a["type"], a["details"], a["severity"])
        )
    conn.commit()
    conn.close()

def get_all_anomalies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM anomalies ORDER BY timestamp DESC")
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "sensor_id": r[1],
            "timestamp": str(r[2]),
            "type": r[3],
            "details": r[4],
            "severity": r[5]
        }
        for r in rows
    ]
