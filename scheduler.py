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
        frequency: int = 60,
    ) -> None:
        if start > end:
            raise ValueError("Start date cannot be greater than the end date")
        elif frequency <= 0:
            raise ValueError("Frequency cannot be zero or negative")

        new_job = {
            "method": methodToRun,
            "days": day_of_week,
            "start": start,
            "end": end,
            "frequency": frequency,
        }
        self.jobs.append(new_job)
