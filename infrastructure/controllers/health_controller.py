"""Health check controller"""
from fastapi import APIRouter
from infrastructure.models.response_models import HealthResponse, RootResponse

router = APIRouter(tags=["Health"])


@router.get("/", response_model=RootResponse)
async def root():
    """Root endpoint"""
    return RootResponse(message="FastAPI está funcionando correctamente")


@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(status="healthy")

