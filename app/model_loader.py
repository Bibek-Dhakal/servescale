import logging
from typing import Any

import numpy as np
import onnxruntime as ort

from app.config import settings

logger = logging.getLogger(__name__)


class ONNXModelWrapper:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.session = None
        self.input_name = None
        self.output_name = None

    def load(self) -> None:
        logger.info(f"Loading model from {self.model_path}")
        try:
            # CPU Execution provider for lightweight local k8s scaling
            self.session = ort.InferenceSession(self.model_path, providers=["CPUExecutionProvider"])
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError(f"Could not initialize ONNX runtime session: {e}") from e

    def predict(self, input_data: list[list[float]]) -> list[Any]:
        if not self.session:
            raise RuntimeError("Model is not loaded.")

        # Convert to expected tensor format (float32)
        input_array = np.array(input_data, dtype=np.float32)
        result = self.session.run([self.output_name], {self.input_name: input_array})

        # result[0] contains the output predictions
        return result[0].tolist()


# Singleton instance
model_instance = ONNXModelWrapper(settings.model_path)
