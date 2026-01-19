import asyncio
import route
import image
from scheduler import Scheduler

from pathlib import Path


async def record_route(route_name, from_address: str, to_address):
    if not route_name:
        raise ValueError("route_name is not given for run_route")
    else:
        print(f"Recording route {route_name} from {from_address} to {to_address}")

    route_response = await route.save_route_by_address(
        route_name, [from_address, to_address]
    )

    encoded_polyline = route.get_encoded_polyline(route_response)
    response = await image.download_image(encoded_polyline=encoded_polyline)

    formatted_date_name = route_response["file"]["formatted_date_name"]

    image.save_image(route_name, response, formatted_date_name=formatted_date_name)


async def run_jobs_from_auto_run_list():
    run_file_name = "auto_run_list.py"
    path = Path(run_file_name)

    if not path.is_file():
        return
    import auto_run_list

    export_list = auto_run_list.export_list

    if not export_list:
        return

    s = Scheduler()

    for job_list in export_list:
        route_name = job_list[0]
        from_address = job_list[1]
        to_address = job_list[2]
        days = job_list[3]
        start_hour = job_list[4]
        start_minute = job_list[5]
        end_hour = job_list[6]
        end_minute = job_list[7]
        frequency = job_list[8]
        time_zone = job_list[9]

        if (
            route_name
            and from_address
            and to_address
            and days
            and start_hour >= 0
            and start_minute >= 0
            and end_hour >= 0
            and end_minute >= 0
            and frequency >= 0
        ):

            async def run_job():
                await record_route(route_name, from_address, to_address)

            s.add_job(
                run_job,
                days,
                start_hour,
                start_minute,
                end_hour,
                end_minute,
                frequency,
                time_zone,
            )

    await s.run()


if __name__ == "__main__":
    asyncio.run(run_jobs_from_auto_run_list())
