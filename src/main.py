"""
main.py
"""

import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv

from .routes import (
    heatmap,
    video_retention_peaks,
)
from .services.init_services import init_services

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


app = FastAPI(
    title="YouTube Search Bot",
    description="A Python-based YouTube search bot using FastAPI and YouTube Data API v3",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    redirect_slashes=False,
)

# Initialize CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize services on startup
@app.on_event("startup")
async def startup_event():
    print("All services initialized successfully")
    logger.info("Starting application...")

    # Initialize Redis and other services
    redis_client = await init_services()

    # Initialize and include all routers

    app.include_router(heatmap.init_routes())
    app.include_router(video_retention_peaks.init_routes(redis_client))

    logger.info("All services initialized successfully")


# Add CORS middleware to the FastAPI ap
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run with Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
