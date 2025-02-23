from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/1",
    backend=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/2",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Task settings
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    # Queue settings
    task_default_queue="default",
    task_queues={
        "default": {
            "exchange": "default",
            "routing_key": "default",
        },
        "parsing": {
            "exchange": "parsing",
            "routing_key": "parsing",
        },
        "analysis": {
            "exchange": "analysis",
            "routing_key": "analysis",
        },
    },
    # Routing
    task_routes={
        "app.tasks.analysis.parse_website": {"queue": "parsing"},
        "app.tasks.analysis.run_analysis": {"queue": "analysis"},
        "app.tasks.analysis.generate_recommendations": {"queue": "analysis"},
    },
    # Result backend settings
    result_expires=60 * 60 * 24,  # 24 hours
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    # Beat settings (for periodic tasks)
    beat_schedule={},
)

# Optional: configure Celery logging
celery_app.conf.update(
    worker_hijack_root_logger=False,
    worker_log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    worker_task_log_format="%(asctime)s - %(name)s - %(levelname)s - %(task_name)s[%(task_id)s] - %(message)s",
)
