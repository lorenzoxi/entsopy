import logging

logging.basicConfig(
    filename="./entsopy/data/logs/std.log",
    format="[%(asctime)s] %(message)s",
    filemode="a+",
    force=True,
)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
