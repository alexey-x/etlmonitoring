import traceback
import schedule
import time
import logging

from src.adapters import logger
from src.services import notify_monitoring_alive
from src.collectors import Collector

from src.control_objects import (
    SegmentMODB,
    MOOffersAgg,
    ScenarioMODB,
    ScoreAltScoreLTV,
    SegmentPilotCommRotation,
    SegmentToMO,
    RotationToMO,
    ResultsMOToMA,
)

CONTROL_OBJECTS = [
    SegmentMODB,
    ScenarioMODB,
    ScoreAltScoreLTV,
    SegmentPilotCommRotation,
    SegmentToMO,
    RotationToMO,
    ResultsMOToMA,
    MOOffersAgg,
]


def main(logger: logging.Logger) -> None:
    logger.info("initialize tasks")
    tasks = [Collector(obj, logger) for obj in CONTROL_OBJECTS]

    logger.info("schedule tasks")
    for task in tasks:
        # the meaning of "control_object.run_on_schedule" is like the string below
        # schedule.every().hour.at(":30").do(task.check_new) -- every control_object has its schedule
        task.control_object.run_on_schedule(task.check_new)

    schedule.every().day.at("08:45").do(notify_monitoring_alive)
    logger.info("start eternal loop")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    logger.info("etlmonitoring started")
    try:
        main(logger)
    except Exception as er:
        logger.error("got initialization error")
        logger.error(f"reason: {er}  {traceback.format_exc()}")
