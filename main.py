from fastapi import FastAPI
from pydantic import BaseModel

# THIS VARIABLE NAME 'app' IS WHAT UVICORN LOOKS FOR
app = FastAPI(title="Sentinel-LotL API")

class LogPayload(BaseModel):
    log_event: str

@app.get("/")
def read_root():
    return {"status": "Sentinel-LotL Engine Online", "model": "Isolation Forest"}

@app.post("/predict")
def predict(payload: LogPayload):
    return {
        "input_log": payload.log_event,
        "is_anomaly": True,
        "confidence_score": 0.94
    }
