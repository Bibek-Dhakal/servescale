# Architecture & Optimization Flow

## Inference Optimization
ServeScale employs **ONNX Runtime (CPUExecutionProvider)** coupled with **Dynamic Quantization**.
Rather than serving dense 32-bit floating point models directly via PyTorch, the workflow:
1. Translates the model into `.onnx` representation.
2. Applies 8-bit dynamic integer quantization to weights (`QUInt8`), significantly reducing container memory footprint.
3. Serves the output without an active PyTorch overhead dependency.

## System Topology

> 📸 **Visual Diagram:** View the graphical version of this topology in our [v0.2.0 Run Report](../runs/v0.2.0_run.md#1-architecture-overview).

```mermaid
graph TD;
    Client[Locust / Client] -->|HTTP POST| LB[K8s Service / Load Balancer]
    LB --> Pod1[Replica 1]
    LB --> Pod2[Replica 2]
    LB --> Pod3[Replica 3]

    subgraph "Kubernetes Deployment"
        Pod1 --> ORT1[ONNX Runtime]
        Pod2 --> ORT2[ONNX Runtime]
        Pod3 --> ORT3[ONNX Runtime]
    end

    ORT1 --> Model[(Quantized ONNX)]
    ORT2 --> Model
    ORT3 --> Model
```
