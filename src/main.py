"""
main.py
"""

import logging
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response, status
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
    title="Retention Peaks API",
    description="API for analyzing video retention data",
    version="1.0.0",
)

# Initialize CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Retention Peaks API is up and running!"}


@app.get("/health")
async def health_check():
    return Response(content="OK", status_code=status.HTTP_200_OK)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting application...")
    await init_services()
    app.include_router(heatmap.init_routes())
    app.include_router(video_retention_peaks.init_routes())
    logger.info("All services initialized successfully")
