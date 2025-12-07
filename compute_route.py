import os
import asyncio
from dotenv import load_dotenv

from google.maps.routing_v2 import RoutesAsyncClient
from google.maps.routing_v2.types import (
    ComputeRoutesRequest, 
    Waypoint, 
    Location, 
    RouteTravelMode
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
            travel_mode=RouteTravelMode.DRIVE
        )

        field_mask = FieldMask(paths=["routes.duration", "routes.distance_meters"])

        try:
            response = await client.compute_routes(
                request=request,
                metadata=[("x-goog-fieldmask", field_mask.paths[0])]
            )

            if response.routes:
                route = response.routes[0]
                print(f"Distaince: {route.distance_meters} meters")
                print(f"Async Route Duration: {route.duration.seconds} seconds")
            else:
                print("No routes found")

        except Exception as ex:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(compute_route())