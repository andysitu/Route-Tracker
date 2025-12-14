import time
import datetime
from typing import Callable, List


class Scheduler:
    def __init__(self):
        self.jobs: List = []

    def add_scheduler(
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
        self.jobs.append(new_job)
