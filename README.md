# ServeScale 🚀

**ServeScale** is a horizontally scalable, latency-optimized machine learning model serving system built on Kubernetes. It demonstrates production-serving competence by providing orchestrated scale, explicit inference optimization, and zero-downtime updates.

## 🌟 Key Features
- **Kubernetes Orchestration**: Horizontal scaling with min/max replicas and native load balancing.
- **Inference Optimization**: Leverages ONNX Runtime and Dynamic Quantization to minimize latency and memory footprint.
- **Zero-Downtime Rollouts**: Configured K8s deployment strategy with liveness/readiness probes ensuring no requests are dropped during updates.
- **Load Verification**: Integrated `Locust` suite to measure concurrency limits, latency, and error rates before and after optimization.

## 📚 Documentation Index
- [Code Quality & Setup](CODE_QUALITY.md)
- [Usage & Configuration](docs/usage/README.md)
- [Architecture & Data Flow](docs/architecture/README.md)
- [Testing & Quality Assurance](docs/testing/README.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🛠 Quick Start

### 1. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,model-gen]"
cp .env.example .env
```

### 2. Generate Optimized Models
```bash
python scripts/generate_model.py
```

### 3. Run Locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 Kubernetes Deployment
ServeScale is designed to run on a local Kubernetes cluster (like Minikube or Kind) or any cloud provider.
For detailed instructions on cluster setup, image loading, and rolling updates, see the [Usage Guide](docs/usage/README.md).
