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
1. Ensure the API is active (via uvicorn or k8s port-forwarding).
2. Start Locust:
   ```bash
   locust -f load_tests/locustfile.py --host=http://localhost:8000
   ```
3. Navigate to `http://localhost:8089` to monitor requests per second (RPS), connection errors, and response times.

**Verification Steps:**
- Run the Locust load test at 50 concurrent users.
- Observe baseline metrics.
- Trigger a rolling K8s update.
- Ensure **0 Connection Failures** populate during the transition phase.
