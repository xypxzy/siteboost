from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.core.rate_limit import check_rate_limit
from app.core.redis import RedisClient
from app.models.user import User
from app.schemas.analysis import AnalysisCreate, AnalysisResponse, AnalysisDetail
from app.services import parser_service, analyzer_service
from app.core.celery_app import celery_app

router = APIRouter()


@router.post("/", response_model=AnalysisResponse)
async def create_analysis(
    *,
    db: Session = Depends(deps.get_db),
    redis: RedisClient = Depends(deps.get_redis),
    analysis_in: AnalysisCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new analysis following the sequence:
    1. Rate limit check
    2. Create analysis record
    3. Schedule analysis task
    """
    # Check rate limit
    if not await check_rate_limit(redis, current_user.id):
        raise HTTPException(
            status_code=429, detail="Rate limit exceeded. Please try again later."
        )

    # Create analysis record
    analysis = await parser_service.create_analysis_request(
        db=db,
        url=analysis_in.url,
        settings=analysis_in.settings,
        user_id=current_user.id,
    )

    # Schedule analysis task
    task = celery_app.send_task(
        "app.tasks.analysis.start_analysis_pipeline", args=[str(analysis.id)]
    )

    return JSONResponse(
        status_code=202,
        content={
            "taskId": task.id,
            "analysisId": str(analysis.id),
            "status": "accepted",
            "message": "Analysis task scheduled successfully",
        },
    )


@router.get("/{analysis_id}", response_model=AnalysisDetail)
async def get_analysis(
    *,
    db: Session = Depends(deps.get_db),
    redis: RedisClient = Depends(deps.get_redis),
    analysis_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get analysis results with caching:
    1. Check cache
    2. Verify access
    3. Load from database if not in cache
    """
    # Try to get from cache
    cached_result = await redis.get(f"analysis:{analysis_id}")
    if cached_result:
        return cached_result

    # Get from database
    analysis = await analyzer_service.get_complete_analysis(
        db=db, analysis_id=analysis_id, user_id=current_user.id
    )

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    # Cache the result
    await redis.set(f"analysis:{analysis_id}", analysis.dict(), expire=3600)  # 1 hour

    return analysis
