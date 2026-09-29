import logging
import os
import warnings

import torch
import torch.nn as nn
from onnxruntime.quantization import QuantType, quantize_dynamic, shape_inference
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Suppress noisy PyTorch internal ONNX diagnostic logs
logging.getLogger("torch.onnx").setLevel(logging.ERROR)


# Define a simple PyTorch Neural Network
class SimpleNN(nn.Module):
    def __init__(self, input_dim: int):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return self.sigmoid(out)


def train_and_export():
    # 1. Generate synthetic dataset
    print("Generating synthetic data...")
    X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

    # 2. Train the model
    print("Training PyTorch model...")
    model = SimpleNN(input_dim=10)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    model.train()
    for _ in range(50):
        optimizer.zero_grad()
        outputs = model(X_train_t)
        loss = criterion(outputs, y_train_t)
        loss.backward()
        optimizer.step()

    # 3. Export to Base ONNX
    os.makedirs("models", exist_ok=True)
    base_onnx_path = "models/model.onnx"
    preprocessed_onnx_path = "models/model_prep.onnx"
    quantized_onnx_path = "models/model_quantized.onnx"

    print(f"Exporting base model to {base_onnx_path}...")
    model.eval()
    dummy_input = torch.randn(1, 10, dtype=torch.float32)

    # Ignore the noisy Dynamo/dynamic_axes warnings in newer PyTorch versions
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        torch.onnx.export(
            model,
            dummy_input,
            base_onnx_path,
            export_params=True,
            opset_version=18,
            do_constant_folding=False,  # Fixes the dynamic_axes shape inference bugs
            input_names=["input"],
            output_names=["output"],
            dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
        )

    # 4. Preprocess for Quantization
    print("Running ONNX shape inference preprocessing...")
    # Suppress ONNX shape inference warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        shape_inference.quant_pre_process(
            input_model_path=base_onnx_path,
            output_model_path=preprocessed_onnx_path,
            skip_symbolic_shape=False,
        )

    # 5. Apply Dynamic Quantization (Optimization Step)
    print(f"Applying dynamic quantization to {quantized_onnx_path}...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        quantize_dynamic(
            model_input=preprocessed_onnx_path,
            model_output=quantized_onnx_path,
            weight_type=QuantType.QUInt8,
        )

    # Cleanup temporary preprocessed file
    if os.path.exists(preprocessed_onnx_path):
        os.remove(preprocessed_onnx_path)

    print("Model generation and optimization complete! 🎉")
    print(f"- Base Size: {os.path.getsize(base_onnx_path) / 1024:.2f} KB")
    print(f"- Quantized Size: {os.path.getsize(quantized_onnx_path) / 1024:.2f} KB")


if __name__ == "__main__":
    train_and_export()
