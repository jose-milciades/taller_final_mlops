import json
import os
from pathlib import Path

import pytest

from app.model import OnnxModel


def test_downloaded_model_meets_metric_threshold():
    model_path = Path(os.getenv("MODEL_PATH", "artifacts/model.onnx"))
    test_data_path = Path(os.getenv("TEST_DATA_PATH", "artifacts/test_data.json"))

    if not model_path.exists() or not test_data_path.exists():
        pytest.skip("Downloaded model and test data are not available locally.")

    rows = json.loads(test_data_path.read_text(encoding="utf-8"))
    inputs = [row["inputs"] for row in rows]
    expected = [row["expected"] for row in rows]

    model = OnnxModel(model_path)
    predictions = [row[0] for row in model.predict(inputs)]
    mean_absolute_error = sum(
        abs(target - prediction)
        for target, prediction in zip(expected, predictions)
    ) / len(expected)

    assert mean_absolute_error < 0.001
