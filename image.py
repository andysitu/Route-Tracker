import requests
import httpx
import os


async def download_image(encoded_polyline):
    url = (
        "https://maps.googleapis.com/maps/api/staticmap?"
        f"size=600x400&"
        f"path=color:0x0000FF|weight:5|enc:{encoded_polyline}&"
        f"key={os.environ['GOOGLE_API_KEY']}"
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, follow_redirects=True)
            # response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error fetching static map: {e}")
            print(f"Response content: {e.response.text}")
        except httpx.RequestError as e:
            print(f"An error occurred while requesting the map: {e}")

    response = requests.get(url)

    return response
