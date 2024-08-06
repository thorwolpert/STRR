from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .job import run

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=run, trigger=IntervalTrigger(hours=1), next_run_time=datetime.now()
    )
    scheduler.start()
