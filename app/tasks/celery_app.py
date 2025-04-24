from celery import Celery
from celery.schedules import crontab

from app.config import settings


celery = Celery(
    "tasks", 
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        'app.tasks.tasks',
        'app.tasks.scheduled',
        ]
)

celery.conf.beat_schedule = {
    'luboe_nazvanie': {
        "task": "periodic_task",
        "schedule": 20, #секунды
         # "schedule": crontab(minute='15', hour='01'),
    },
    'reminder_1': {
        "task": "reminder_0900",
        "schedule": 60, #секунды
    #    "schedule": crontab(minute='31', hour='09'),
    },
    'reminder_2': {
        "task": "reminder_1530",
        "schedule": 35, #секунды
    #    "schedule": crontab(minute='32', hour='09'),
    },
}