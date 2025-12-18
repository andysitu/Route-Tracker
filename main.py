import asyncio
import route
import image
from scheduler import Scheduler


async def run_route(from_address: str, to_address):
    route_response = await route.save_route_by_address([from_address, to_address])

    encoded_polyline = route.get_encoded_polyline(route_response)
    response = await image.download_image(encoded_polyline=encoded_polyline)

    formatted_date_name = route_response["file"]["formatted_date_name"]

    image.save_image(response, formatted_date_name=formatted_date_name)
