import httpx
import os
import route


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
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error fetching static map: {e}")
            print(f"Response content: {e.response.text}")
        except httpx.RequestError as e:
            print(f"An error occurred while requesting the map: {e}")


def save_image(route_name: str, response, formatted_date_name):
    if response.status_code == 200:

        folder_path = route.getFolderpath(route_name)

        filepath = os.path.join(folder_path, f"{formatted_date_name}.png")

        with open(filepath, "wb") as file:
            file.write(response.content)
