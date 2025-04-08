from fastapi import FastAPI
from anomalies_routes import router

app = FastAPI(title="Anomaly Detection Service", version="1.0")

app.include_router(router)
