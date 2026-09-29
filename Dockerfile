FROM python:3.11-slim

WORKDIR /app

# Copy necessary files for building the package via pyproject.toml
COPY pyproject.toml README.md ./
COPY ./app /app/app

# Install application and dependencies
RUN pip install --no-cache-dir .

# Copy models separately (as they can be large/frequently updated independently)
COPY ./models /app/models

# Use a non-root user for security
RUN useradd -m serveuser
USER serveuser

EXPOSE 8000

# Start API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
