# Testing & Quality Assurance

## Unit Testing

Run the Python test suite directly using Pytest:

```bash
pytest tests/
```

Tests simulate incoming JSON parsing correctly mapping to inference requests.

## Performance Load Testing

To explicitly measure inference latency and prove no-dropped-connections during a K8s rolling update, use `Locust`.

**Execution:**

1. Ensure the API is active (via Uvicorn or k8s port-forwarding).
2. **Start Locust:**

    * **If using Port Forwarding (`localhost:8000`):**
      ```bash
      locust -f load_tests/locustfile.py --host=http://localhost:8000
      ```

    * **If using Minikube NodePort:**
      Replace `<MINIKUBE_URL>` with the output from `minikube service servescale-service --url`:
      ```bash
      locust -f load_tests/locustfile.py --host=<MINIKUBE_URL>
      ```
      Example
      ```bash
      locust -f load_tests/locustfile.py --host=http://127.0.0.1:65056
      ```

3. Navigate to [http://localhost:8089](http://localhost:8089) to monitor requests per second (RPS), connection errors,
   and response times.

**Verification Steps:**

- Run the Locust load test at 50 concurrent users.
- Observe baseline metrics.
- Trigger a rolling K8s update.
- Ensure **0 Connection Failures** populate during the transition phase.

**Verify Zero-Downtime Rollout**:

- While Locust is actively running (e.g., 50 concurrent users), trigger a rollout:

```bash
docker tag servescale:v1 servescale:v2
# Load v2 image into minikube/kind
kubectl set image deployment/servescale-deployment api=servescale:v2
```

- Watch the pods: `kubectl get pods -w`
- Observe Locust. You must see **0 errors** (no dropped requests) while old pods terminate and new pods take over
  traffic.
