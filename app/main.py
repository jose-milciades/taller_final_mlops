from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.config import Settings, get_settings
from app.logging import append_prediction
from app.model import OnnxModel

app = FastAPI(title="ONNX Prediction API", version="0.1.0")


class PredictionRequest(BaseModel):
    inputs: list[list[float]] = Field(..., min_length=1)


class PredictionResponse(BaseModel):
    environment: str
    prediction: list


@lru_cache
def get_model(model_path: str) -> OnnxModel:
    return OnnxModel(get_settings().model_path)


@app.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "environment": settings.app_env}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    settings: Settings = get_settings()
    try:
        model = get_model(str(settings.model_path))
        prediction = model.predict(request.inputs)
        append_prediction(
            log_path=settings.predictions_log_path,
            payload=request.model_dump(),
            prediction=prediction,
            app_env=settings.app_env,
            remote_uri=settings.predictions_log_uri,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return PredictionResponse(environment=settings.app_env, prediction=prediction)
