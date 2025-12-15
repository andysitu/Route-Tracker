import time
import datetime
from typing import Callable, Dict, List
import inspect


class Scheduler:
    def __init__(self):
        self.jobs: Dict = {}
        self._current_id: int = 0

    def is_func_async(method):
        return inspect.iscoroutinefunction(method)

    def add_job(
        self,
        methodToRun: Callable,
        days_of_week: List[int],
        start_hour: int,
        end_hour: int,
        min_frequency: int = 1,  # integer per minute frequency
    ) -> None:
        if start_hour > start_hour:
            raise ValueError("Start date cannot be greater than the end date")
        elif min_frequency < 0:
            # Minute accuracy
            # Scheduling might not be accurate enough under a minute
            raise ValueError("Frequency cannot be less than 1")

        new_job = {
            "method": methodToRun,
            "days_of_week": days_of_week,
            "start_hour": start_hour,
            "end_hour": end_hour,
            "frequency": min_frequency,
        }
        self.jobs[self.current_id] = new_job
        self.current_id += 1

    def remove_job(self, id: int):
        if int in self.jobs:
            del self.jobs[id]
