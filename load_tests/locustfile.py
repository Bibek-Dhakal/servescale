import random

from locust import HttpUser, between, task


class InferenceUser(HttpUser):
    # Simulates users hitting the API with a 0.5 - 2 second delay between requests
    wait_time = between(0.5, 2.0)

    @task(3)
    def predict_endpoint(self):
        """Simulate sending batches to the prediction endpoint."""
        # Generate random batch of 1 to 5 items, each with 10 features
        batch_size = random.randint(1, 5)
        features = [[random.random() for _ in range(10)] for _ in range(batch_size)]

        payload = {"features": features}

        with self.client.post("/predict", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}: {response.text}")

    @task(1)
    def health_endpoint(self):
        """Periodically check the health endpoint."""
        self.client.get("/health")
