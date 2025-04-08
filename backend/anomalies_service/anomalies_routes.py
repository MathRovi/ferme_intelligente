from fastapi import APIRouter, HTTPException
import logging
from anomalies_service.anomalies_utils import (
    get_recent_measurements,
    detect_anomalies,
    insert_anomalies,
    get_all_anomalies
)

router = APIRouter()

@router.post("/api/v1/analyze")
def analyze():
    try:
        measurements = get_recent_measurements()
        anomalies = detect_anomalies(measurements)
        insert_anomalies(anomalies)
        return {"message": f"{len(anomalies)} anomalies détectées."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/anomalies")
def list_anomalies():
    try:
        return get_all_anomalies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
