import time
import datetime
from typing import Callable, Dict, List
import inspect


class Scheduler:
    def __init__(self):
        self.jobs: Dict = {}
        self._current_id: int = 0

    def is_func_async(self, method):
        return inspect.iscoroutinefunction(method)

    def add_job(
        self,
        methodToRun: Callable,
        days_of_week: List[int],
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        min_frequency: int = 1,  # integer per minute frequency
    ) -> None:
        if start_hour > end_hour:
            raise ValueError("Start date cannot be greater than the end date")
        elif start_hour == end_hour and start_minute > end_minute:
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
        self.jobs[self._current_id] = new_job
        self._current_id += 1

    def remove_job(self, id: int):
        if int in self.jobs:
            del self.jobs[id]

    async def run(self):
        while True:
            now = datetime.datetime.now()

            for job in self.jobs.values():
                start_hour = job["start_hour"]
                end_hour = job["end_hour"]
                start_minute = job["start_minute"]
                end_minute = job["end_minute"]
                frequency = job["frequency"]
                days_of_week = job["days_of_week"]
                method = job["method"]

                if not (start_hour <= now.hour <= end_hour):
                    continue
                elif now.hour == start_hour and now.minute < start_minute:
                    continue
                elif now.hour == end_hour and now.minute > end_minute:
                    continue
                elif now.minute % frequency != 0:
                    continue
                elif now.weekday() not in days_of_week:
                    continue

                if self.is_func_async(method):
                    await method()
                else:
                    method()

            time.sleep(60)
