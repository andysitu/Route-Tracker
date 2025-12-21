import asyncio
import route
import image
from scheduler import Scheduler


async def run_route(route_name, from_address: str, to_address):
    if not route_name:
        raise ValueError("route_name is not given for run_route")

    route_response = await route.save_route_by_address(
        route_name, [from_address, to_address]
    )

    encoded_polyline = route.get_encoded_polyline(route_response)
    response = await image.download_image(encoded_polyline=encoded_polyline)

    formatted_date_name = route_response["file"]["formatted_date_name"]

    image.save_image(route_name, response, formatted_date_name=formatted_date_name)
