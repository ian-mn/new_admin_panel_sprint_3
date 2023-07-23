from apscheduler.schedulers.blocking import BlockingScheduler
from settings import get_settings

from etl import ETL

sched = BlockingScheduler()


@sched.scheduled_job("interval", id="start_etl", minutes=1)
def start_elt():
    etl = ETL()
    etl.try_start()


if __name__ == "__main__":
    start_elt()

    if get_settings().automatic_updates:
        sched.start()
