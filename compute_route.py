import os
import asyncio
from dotenv import load_dotenv

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

async def compute_route():
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("API KEY NOT FOUND IN ENV FILE")

    async with RoutesAsyncClient() as client:
        origin_latlng = LatLng(latitude=34.0522, longitude=-118.2437)
        destination_latlng = LatLng(latitude=34.0040, longitude=-118.4973)

        origin = Waypoint(location=Location(lat_lng=origin_latlng))
        destination = Waypoint(location=Location(lat_lng=destination_latlng))

        request = ComputeRoutesRequest(
            origin=origin,
            destination=destination,
            travel_mode=RouteTravelMode.DRIVE,
            routing_preference=RoutingPreference.TRAFFIC_AWARE_OPTIMAL,
        )

        paths = [
            "routes.duration",
            "routes.distance_meters",
            "routes.polyline.encoded_polyline",
            "geocodingResults",
        ]
        field_mask = FieldMask(paths=paths)
        # mask_string = ",".join(paths)
        mask_string = "*"

        try:
            response = await client.compute_routes(
                request=request, metadata=[("x-goog-fieldmask", mask_string)]
            )

            if response.routes:

                # response_json = json_format.MessageToJson(
                #     response.routes[0],
                #     indent=2,  # Use indent=2 for nicely formatted, readable output
                # )
                response_json = type(response).to_json(response)

                print("-------- ROUTES API RESPONSE (JSON) --------")
                print(response_json)
            else:
                print("No routes found")

        except Exception as ex:
            print(f"An error occurred: {ex}")

if __name__ == "__main__":
    asyncio.run(compute_route())