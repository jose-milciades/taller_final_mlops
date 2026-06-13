import json
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper


def create_linear_onnx_model(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    x = helper.make_tensor_value_info("input", TensorProto.FLOAT, [None, 4])
    y = helper.make_tensor_value_info("output", TensorProto.FLOAT, [None, 1])

    weights = numpy_helper.from_array(
        np.array([[0.2], [0.1], [0.4], [0.3]], dtype=np.float32),
        name="weights",
    )
    bias = numpy_helper.from_array(np.array([0.5], dtype=np.float32), name="bias")

    graph = helper.make_graph(
        [
            helper.make_node("MatMul", ["input", "weights"], ["weighted"]),
            helper.make_node("Add", ["weighted", "bias"], ["output"]),
        ],
        "linear_model",
        [x],
        [y],
        initializer=[weights, bias],
    )
    model = helper.make_model(
        graph,
        producer_name="sample-artifacts",
        opset_imports=[helper.make_operatorsetid("", 19)],
    )
    model.ir_version = 10
    onnx.save(model, path)


def create_test_data(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {"inputs": [1, 2, 3, 4], "expected": 3.3},
        {"inputs": [0, 1, 1, 2], "expected": 1.6},
        {"inputs": [2, 0, 1, 1], "expected": 1.6},
    ]
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def main() -> None:
    create_linear_onnx_model(Path("artifacts/model.onnx"))
    create_test_data(Path("artifacts/test_data.json"))
    print("Generated artifacts/model.onnx and artifacts/test_data.json")


if __name__ == "__main__":
    main()
