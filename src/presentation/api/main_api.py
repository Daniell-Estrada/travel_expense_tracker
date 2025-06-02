import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from infrastructure.database import DatabaseConnection
from presentation.api.controllers import (dashboard_router, expense_router,
                                          report_router, trip_router)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    logger.info("Starting Travel Expense Tracker API...")

    try:
        DatabaseConnection()
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise e

    yield

    logger.info("Shutting down Travel Expense Tracker API...")


app = FastAPI(
    title=settings.app_name,
    description="API for tracking travel expenses with clean architecture",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


routers = {
    "dashboard": dashboard_router,
    "expenses": expense_router,
    "reports": report_router,
    "trips": trip_router,
}

for tag, router in routers.items():
    app.include_router(router, prefix=settings.API_V1_PREFIX, tags=[tag])


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/api/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    uvicorn.run(
        "main_api:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
