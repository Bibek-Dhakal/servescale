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

**Prerequisites:** [Minikube](https://minikube.sigs.k8s.io/) or [Kind](https://kind.sigs.k8s.io/) running locally.

1. **Build and Tag Image:**

```bash
docker build -t servescale:v1 .

```

2. **Load Image into Minikube/Kind:**

```bash
minikube image load servescale:v1
# OR
kind load docker-image servescale:v1

```

3. **Deploy Resources:**

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

```

4. **Access the Service:**
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

## Rolling Update / Zero-Downtime Deployment

To deploy a new model or app version without dropping traffic:

1. Build the new version: `docker build -t servescale:v2 .`
2. Load it into your cluster node: `minikube image load servescale:v2`
3. Update the deployment image:

```bash
kubectl set image deployment/servescale-deployment api=servescale:v2

```

4. Kubernetes will begin a rolling update, respecting the `maxUnavailable: 0` and `maxSurge: 1` directives, alongside
   readiness probes. Verify it using this command:

```bash
kubectl rollout status deployment/servescale-deployment

```
