import os
from dotenv import load_dotenv
import json
import json_lib
import datetime

from google.maps.routing_v2 import RoutesAsyncClient
from google.maps.routing_v2.types import (
    ComputeRoutesRequest,
    Waypoint,
    Location,
    RouteTravelMode,
    RoutingPreference,
)
from google.type.latlng_pb2 import LatLng
from google.protobuf.field_mask_pb2 import FieldMask


load_dotenv()


def getDateFilename():
    current = datetime.datetime.now()
    formatted_name = current.strftime("%Y%m%d_%H%M%S")
    dateString = formatted_name.split("_")[0]
    timeString = formatted_name.split("_")[1]
    return formatted_name, dateString, timeString


# paths = [
#     "routes.duration",
#     "routes.distance_meters",
#     "routes.polyline.encoded_polyline",
#     "geocodingResults",
# ]
async def compute_route(
    addresses: list[str] | None = None,
    latlangs: list[float] | None = None,
    paths: list[str] | None = None,
):
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("API KEY NOT FOUND IN ENV FILE")

    async with RoutesAsyncClient() as client:
        location = {}
        if addresses and len(addresses) >= 2:
            origin = Waypoint(address=addresses[0])
            destination = Waypoint(address=addresses[1])

            location = {
                "origin": {
                    "address": addresses[0],
                },
                "destination": {"address": addresses[1]},
            }
        elif latlangs and len(latlangs) >= 4:
            origin_latlng = LatLng(latitude=latlangs[0], longitude=latlangs[1])
            destination_latlng = LatLng(latitude=latlangs[2], longitude=latlangs[3])

            origin = Waypoint(location=Location(lat_lng=origin_latlng))
            destination = Waypoint(location=Location(lat_lng=destination_latlng))

            location = {
                "origin": {"coordinates": [latlangs[0], latlangs[1]]},
                "destination": {"coordinates": [latlangs[2], latlangs[3]]},
            }
        else:
            raise ValueError("Incorrect parameters provided to compute_route")

        request = ComputeRoutesRequest(
            origin=origin,
            destination=destination,
            travel_mode=RouteTravelMode.DRIVE,
            routing_preference=RoutingPreference.TRAFFIC_AWARE_OPTIMAL,
        )

        if paths:
            field_mask = FieldMask(paths=paths)
            mask_string = ",".join(paths)
        else:
            mask_string = "*"

        try:
            response = await client.compute_routes(
                request=request, metadata=[("x-goog-fieldmask", mask_string)]
            )

            if response.routes:
                response_json_str = type(response).to_json(response)
                response_json = json.loads(response_json_str)
                response_json["location"] = location

                return response_json
            else:
                print("No routes found")

        except Exception as ex:
            print(f"An error occurred: {ex}")


async def save_route_by_address(
    addresses: list[str],
):
    response = await compute_route(addresses=addresses)
    formatted_name, dateString, _ = getDateFilename()

    if response:
        json_lib.save_json(response, f"data/{dateString}", f"{formatted_name}.json")
    return response


async def save_route_by_coordinates(latlangs: list[float]):
    response = await compute_route(latlangs=latlangs)

    current = datetime.datetime.now()
    formatted_name = current.strftime("%Y%m%d_%H%M%S")
    dateString = formatted_name.split("_")[0]

    if response:
        json_lib.save_json(response, f"data/{dateString}", f"{formatted_name}.json")
