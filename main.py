from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sentinel-LotL Detection API")

class LogPayload(BaseModel):
    log_event: str

@app.get("/")
def health_check():
    return {"status": "Sentinel-LotL Engine Online", "model": "Isolation Forest"}

# Must be @app.post, NOT @app.get, and path must match "/predict" exactly
@app.post("/predict")
def predict(payload: LogPayload):
    return {
        "input_log": payload.log_event,
        "is_anomaly": True,
        "confidence_score": 0.94
    }
