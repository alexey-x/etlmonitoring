import logging
import traceback
from typing import Set
import os
import sys

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("."))


from app.src.services import notify_admin
from app.src.control_objects import ControlObject


class Collector:
    def __init__(self, control_object: ControlObject, logger: logging.Logger) -> None:
        self.control_object = control_object()
        self.logger = logger
        self.tracing_data = self.collect()

    def collect(self) -> Set:
        self.logger.info(f"start collect: {self.control_object.__class__.__name__}")
        try:
            result = set(self.control_object.get_data())
            self.logger.info(f"got data: {result}")
        except TypeError:
            result = set()
            self.logger.warning("got None from database - no connection")
        except Exception as er:
            result = set()
            self.logger.error(f"collect error reason: {er} {traceback.format_exc()}")
            notify_admin(event="COLLECT DATA ERROR", data=traceback.format_exc())
        finally:
            self.logger.info(f"end collect: {self.control_object.__class__.__name__}")
            return result

    def check_new(self) -> None:
        new_tracing_data = self.collect()
        self.logger.info(f"start check: {self.control_object.__class__.__name__}")
        try:
            diff_tracing_data = new_tracing_data.difference(self.tracing_data)
            if diff_tracing_data:
                self.control_object.process_data(diff_tracing_data)
                self.tracing_data = new_tracing_data
                self.logger.info(f"length of the new data = {len(diff_tracing_data)}")
            else:
                self.logger.info("-> nothing new <-")
        except Exception as er:
            self.logger.error(f"check error reason: {er} {traceback.format_exc()}")
            notify_admin(event="CHECK NEW DATA ERROR", data=traceback.format_exc())
        finally:
            self.logger.info(f"end check {self.control_object.__class__.__name__}")
