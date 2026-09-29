FROM python:3.11-slim

WORKDIR /app

# Install dependencies using pyproject.toml
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy application code and models
COPY ./app /app/app
COPY ./models /app/models

# Use a non-root user for security
RUN useradd -m serveuser
USER serveuser

EXPOSE 8000

# Start API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
