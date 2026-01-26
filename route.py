import os
from dotenv import load_dotenv
import json
import file_lib
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

from zoneinfo import ZoneInfo


load_dotenv()


def getDateNames(time_zone: str):
    if time_zone:
        now = now = datetime.datetime.now(ZoneInfo(time_zone))
    else:
        now = datetime.datetime.now()

    formatted_date_name = now.strftime("%Y%m%d_%H%M%S")
    date_string = formatted_date_name.split("_")[0]
    time_string = formatted_date_name.split("_")[1]
    return formatted_date_name, date_string, time_string


def get_data_folder_path(route_name, include_date=True):
    _, dateString, _ = getDateNames()
    if route_name:
        path_without_date = f"data/{route_name}"
    else:
        path_without_date = f"data/"

    if include_date:
        path_without_date += "/" + dateString

    return path_without_date


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


def save_response_to_file(route_name: str, response, time_zone: str):
    if response:
        formatted_date_name, date_string, time_string = getDateNames(time_zone)
        response["file"] = {
            "formatted_date_name": formatted_date_name,
            "date_string": date_string,
            "time_string": time_string,
        }

        file_lib.save_json(
            response, get_data_folder_path(route_name), f"{formatted_date_name}.json"
        )
    return response


async def save_route_by_address(route_name: str, addresses: list[str], time_zone: str):
    response = await compute_route(addresses=addresses)
    return save_response_to_file(route_name, response, time_zone)


async def save_route_by_coordinates(
    route_name: str, latlangs: list[float], time_zone: str
):
    response = await compute_route(latlangs=latlangs)
    return save_response_to_file(route_name, response, time_zone)


def get_encoded_polyline(response):
    return response["routes"][0]["polyline"]["encodedPolyline"]
