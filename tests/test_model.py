from app.model import OnnxModel
from tests.conftest import create_linear_onnx_model


def test_model_responds_with_defined_input(tmp_path):
    model_path = tmp_path / "model.onnx"
    create_linear_onnx_model(model_path)

    model = OnnxModel(model_path)
    prediction = model.predict([[1, 2, 3, 4]])

    assert prediction == [[3.3000001907348633]]


def test_model_metric_does_not_drop_below_threshold(tmp_path):
    model_path = tmp_path / "model.onnx"
    create_linear_onnx_model(model_path)
    model = OnnxModel(model_path)

    y_true = [3.3, 1.6]
    y_pred = [row[0] for row in model.predict([[1, 2, 3, 4], [0, 1, 1, 2]])]
    mean_absolute_error = sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)

    assert mean_absolute_error < 0.001
