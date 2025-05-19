"""Video retention peaks service for managing YouTube videos"""

from redis.asyncio import Redis
from fastapi import HTTPException
from src.services.youtube_service import YouTubeService
from src.models.video_retention_peaks import (
    VideoRetentionPeaks,
    VideoRetentionPeaksResponse,
)


class VideoRetentionPeakService:
    """Service for managing YouTube videos retention peaks"""

    def __init__(self, redis_client: Redis | None = None):
        """Initialize video retention peaks service"""
        self.youtube_service = YouTubeService(redis_client)

    async def get_video_retention_peak(
        self, video_id: str
    ) -> VideoRetentionPeaksResponse:
        """Get video retention peaks by video ID"""
        video_retention_peaks = await VideoRetentionPeaks.find_one(
            {"video_id": video_id}
        )

        if not video_retention_peaks:
            raise HTTPException(
                status_code=404, detail="Video retention peaks not found"
            )

        return video_retention_peaks
