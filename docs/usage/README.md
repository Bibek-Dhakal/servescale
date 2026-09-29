# Usage & Configuration

## Environment Variables

Configuration is securely passed through `.env` locally or as ConfigMaps/Secrets in Kubernetes.

| Name                   | Type  | Default                         | Description                          |
|------------------------|-------|---------------------------------|--------------------------------------|
| `PORT`                 | `int` | `8000`                          | Application bind port                |
| `CORS_ALLOWED_ORIGINS` | `str` | `"*"`                           | Comma-separated list of CORS origins |
| `ENVIRONMENT`          | `str` | `"development"`                 | Target execution environment         |
| `MODEL_PATH`           | `str` | `"models/model_quantized.onnx"` | File path to the ONNX model artifact |

## Run Kubernetes Deployments Locally

> 📸 **See it in action:** Visual terminal evidence for all deployment steps can be found in the [v0.2.0 Run Report](../runs/v0.2.0_run.md#5-kubernetes-setup--deployment).

**Prerequisites:** [Minikube](https://minikube.sigs.k8s.io/), [Kind](https://kind.sigs.k8s.io/), or Docker Desktop
running locally.

### 1. Start Your Cluster

* **Minikube Users:**

```bash
minikube start

```

* **Kind Users:**

```bash
kind create cluster --name servescale

```

### 2. Build and Tag Image

```bash
docker build -t servescale:v1 .

```

### 3. Load Image into Minikube/Kind

* **Minikube Users:**

```bash
minikube image load servescale:v1

```

* **Kind Users:**

```bash
kind load docker-image servescale:v1 --name servescale

```

### 4. Deploy Resources

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

```

### 5. Access the Service

**Option A: Port Forwarding (Recommended for `localhost:8000`)**
Run the port-forward command and **keep this terminal window open**:

```bash
kubectl port-forward svc/servescale-service 8000:80

```

Open your browser to access the application endpoints:

* **Interactive API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

**Option B: NodePort Direct Access**
Since the service is exposed as `NodePort: 30000`:

* **Minikube Users:** Get the cluster access URL by running:

```bash
minikube service servescale-service --url

```

Navigate to the returned URL and append `/docs` (e.g., `[http://127.0.0.1:58432/docs](http://127.0.0.1:58432/docs)`).

* **Docker Desktop / Kind Users:** Access directly via [http://localhost:30000/docs](http://localhost:30000/docs).

---

## Daily Workflow: Resuming Work (Without Rebuilding Images)

When returning to an existing environment after stopping Docker or restarting your machine, **do not rebuild or reload
the image**. The Docker image and Kubernetes manifests remain saved inside the cluster storage.

1. **Start the existing cluster:**

* **Minikube:**

```bash
minikube start

```

* **Kind:** Ensure Docker Desktop is running. (Kind cluster containers restart automatically with Docker. If paused, run
  `docker start servescale-control-plane`).


2. **Verify pods are running:**

```bash
kubectl get pods

```

3. **Re-establish connection:**

```bash
kubectl port-forward svc/servescale-service 8000:80

```

*(Re-run `docker build` and `minikube image load` / `kind load` only when source code or model files change.)*

---

## Rolling Update / Zero-Downtime Deployment

To deploy a new model or app version without dropping traffic:

> 📸 **Visual Proof:** See our [Zero-Downtime Rollout K8s execution logs](../runs/v0.2.0_run.md#7-zero-downtime-rollout-execution) ensuring zero HTTP request drops.

1. **Build the new version:**

```bash
docker build -t servescale:v2 .

```

2. **Load it into your cluster node:**

```bash
minikube image load servescale:v2
# OR for Kind:
kind load docker-image servescale:v2 --name servescale

```

3. **Update the deployment image:**

```bash
kubectl set image deployment/servescale-deployment api=servescale:v2

```

4. **Verify rollout status:**
   Kubernetes will begin a rolling update respecting `maxUnavailable: 0` and `maxSurge: 1` directives alongside
   readiness probes. Verify with:

```bash
kubectl rollout status deployment/servescale-deployment

```
