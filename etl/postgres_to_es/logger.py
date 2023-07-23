import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(process)d-%(levelname)s-%(message)s",
    force=True,
)


logger = logging.getLogger()
