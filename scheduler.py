import time
import datetime
from typing import Callable, List


class scheduler:
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
        new_job = {
            "method": methodToRun,
            "days": day_of_week,
            "start": start,
            "end": end,
            "frequency": frequency,
        }
        self.jobs.append(new_job)
