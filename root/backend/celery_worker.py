from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/1",
    backend="redis://localhost:6379/2",
    include=["tasks"]
)

celery_app.conf.timezone = "Asia/Kolkata"

celery_app.conf.beat_schedule = {

    "interview-reminder-daily": {
        "task": "tasks.interview_reminders",
        "schedule": crontab(hour=9, minute=0)
    },
        "monthly-placement-report": {
        "task": "tasks.monthly_placement_report",
        "schedule": crontab(
            day_of_month=1,
            hour=9,
            minute=0
        )
    },

    "monthly-admin-report": {
        "task": "tasks.admin_monthly_report",
        "schedule": crontab(
            day_of_month=1,
            hour=9,
            minute=0
        )
    }

}
