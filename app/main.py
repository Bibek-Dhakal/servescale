from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import settings
from app.model_loader import model_instance


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events to manage the ML model loading."""
    model_instance.load()
    yield
    # Cleanup logic (if any) goes here


app = FastAPI(
    title="ServeScale API",
    description="Scalable, optimized model serving on Kubernetes",
    version="0.1.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.cors_allowed_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True if "*" not in origins else False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    # Dummy feature size for testing (e.g., 10 features)
    features: list[list[float]] = Field(
        ...,
        description="A batch of feature vectors",
        json_schema_extra={"example": [[0.5] * 10, [0.1] * 10]},
    )


class PredictionResponse(BaseModel):
    predictions: list[Any]


@app.get("/health", tags=["Health"])
async def health_check():
    """Liveness/Readiness probe endpoint for Kubernetes."""
    return {"status": "ok", "environment": settings.environment}


@app.post("/predict", response_model=PredictionResponse, tags=["Inference"])
async def predict(request: PredictionRequest):
    """Run inference against the optimized ONNX model."""
    try:
        predictions = model_instance.predict(request.features)
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}") from e
