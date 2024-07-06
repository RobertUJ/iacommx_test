""" Module for celery app """
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["src.tasks"]
)
celery_app.conf.update(
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    auto_discover_tasks=True,
)
