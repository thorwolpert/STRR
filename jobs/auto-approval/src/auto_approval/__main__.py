import os
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from auto_approval.config import get_named_config

from .job import run

if __name__ == "__main__":
    config = get_named_config(os.getenv("FLASK_ENV", "production"))
    interval_time = config.AUTO_APPROVAL_JOB_INTERVAL_MINUTES
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=run,
        trigger=IntervalTrigger(minutes=interval_time),
        next_run_time=datetime.now(),
    )
    scheduler.start()
    try:
        while scheduler.running:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
