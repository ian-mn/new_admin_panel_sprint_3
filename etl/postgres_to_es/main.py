import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from etl import ETL

logging.basicConfig(
    level=logging.INFO,
    format="%(process)d-%(levelname)s-%(message)s",
    force=True,
)


sched = BlockingScheduler()


@sched.scheduled_job("interval", id="start_etl", minutes=1)
def start_elt():
    etl = ETL()
    etl.try_start()


if __name__ == "__main__":
    start_elt()
    sched.start()
