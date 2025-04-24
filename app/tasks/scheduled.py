import asyncio
from app.tasks.celery_app import celery
from app.tasks.reminders.r_bookings import remind_of_bookings

@celery.task(name="periodic_task")
def periodic_task():
    print(12345)

@celery.task(name='reminder_0900')
def reminder_0900():
    asyncio.run(remind_of_bookings(1))


@celery.task(name='reminder_1530')
def remindier_1530():
    asyncio.run(remind_of_bookings(3))
