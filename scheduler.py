import time
import datetime
from typing import Callable, Dict, List


class Scheduler:
    def __init__(self):
        self.jobs: Dict = {}
        self._current_id: int = 0

    def add_job(
        self,
        methodToRun: Callable,
        day_of_week: List[int],
        start: datetime,
        end: datetime,
        frequency: int = 1,  # integer per minute frequency
    ) -> None:
        if start > end:
            raise ValueError("Start date cannot be greater than the end date")
        elif frequency < 0:
            # Minute accuracy
            # Scheduling might not be accurate enough under a minute
            raise ValueError("Frequency cannot be less than 1")

        new_job = {
            "method": methodToRun,
            "days": day_of_week,
            "start": start,
            "end": end,
            "frequency": frequency,
        }
        self.jobs[self.current_id] = new_job
        self.current_id += 1

    def remove_job(self, id: int):
        if int in self.jobs:
            del self.jobs[id]
