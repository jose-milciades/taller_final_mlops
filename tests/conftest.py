from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper


def create_linear_onnx_model(path: Path) -> None:
    x = helper.make_tensor_value_info("input", TensorProto.FLOAT, [None, 4])
    y = helper.make_tensor_value_info("output", TensorProto.FLOAT, [None, 1])

    weights = numpy_helper.from_array(
        np.array([[0.2], [0.1], [0.4], [0.3]], dtype=np.float32),
        name="weights",
    )
    bias = numpy_helper.from_array(np.array([0.5], dtype=np.float32), name="bias")

    matmul = helper.make_node("MatMul", ["input", "weights"], ["weighted"])
    add = helper.make_node("Add", ["weighted", "bias"], ["output"])

    graph = helper.make_graph(
        [matmul, add],
        "linear_model",
        [x],
        [y],
        initializer=[weights, bias],
    )
    model = helper.make_model(
        graph,
        producer_name="tests",
        opset_imports=[helper.make_operatorsetid("", 19)],
    )
    model.ir_version = 10
    onnx.save(model, path)
