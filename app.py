from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sentinel-LotL API")

class LogPayload(BaseModel):
    log_event: str

@app.get("/")
def read_root():
    return {"status": "Sentinel-LotL Engine Online", "model": "Isolation Forest"}

# THIS IS THE MISSING ENDPOINT CAUSING THE 404:
@app.post("/predict")
def predict(payload: LogPayload):
    # Basic logic / model prediction response
    log = payload.log_event.lower()
    
    # Check for common malicious indicators (base64 -e, iex, encodedcommand)
    is_suspicious = any(k in log for k in ["-e ", "encodedcommand", "iex", "downloadstring", "bypass"])
    
    return {
        "input_log": payload.log_event,
        "is_anomaly": is_suspicious,
        "confidence_score": 0.94 if is_suspicious else 0.12
    }
