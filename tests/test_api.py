from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app, get_model
from tests.conftest import create_linear_onnx_model


def test_predict_endpoint_logs_prediction(tmp_path, monkeypatch):
    model_path = tmp_path / "model.onnx"
    log_path = tmp_path / "predicciones_dev.txt"
    create_linear_onnx_model(model_path)

    monkeypatch.setenv("MODEL_PATH", str(model_path))
    monkeypatch.setenv("PREDICTIONS_LOG_PATH", str(log_path))
    monkeypatch.setenv("APP_ENV", "dev")
    get_settings.cache_clear()
    get_model.cache_clear()

    client = TestClient(app)
    response = client.post("/predict", json={"inputs": [[1, 2, 3, 4]]})

    assert response.status_code == 200
    assert response.json()["environment"] == "dev"
    assert log_path.exists()
    assert "prediction" in log_path.read_text(encoding="utf-8")
