
import schedule
import time

import os
import sys

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./app/"))
sys.path.append(os.path.abspath("./tests/e2e/"))
sys.path.append(os.path.abspath("../../"))

for _ in sys.path:
    print(_)



from app.src.adapters import (
    logger,
)
from app.src.collectors import (
    Collector
)
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

def etlmonitoring():
    """
    Run this version to have results every minute at 30 seconds.
    Check results with log file.
    """
    tasks = [Collector(obj, logger) for obj in CONTROL_OBJECTS]

    for task in tasks:
        schedule.every().minute.at(":30").do(task.check_new)
        
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    etlmonitoring()
    
