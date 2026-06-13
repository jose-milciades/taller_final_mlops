from pathlib import Path

import numpy as np
import onnxruntime as ort


class OnnxModel:
    def __init__(self, model_path: Path) -> None:
        if not model_path.exists():
            raise FileNotFoundError(
                f"ONNX model not found at {model_path}. Set MODEL_PATH or download it first."
            )

        self.session = ort.InferenceSession(
            str(model_path),
            providers=["CPUExecutionProvider"],
        )
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def predict(self, inputs: list[list[float]]) -> list:
        input_array = np.asarray(inputs, dtype=np.float32)
        outputs = self.session.run([self.output_name], {self.input_name: input_array})
        return outputs[0].tolist()
