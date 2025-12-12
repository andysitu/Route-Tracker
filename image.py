import requests


def download_image(encoded_polyline):
    url = (
        "https://maps.googleapis.com/maps/api/staticmap?"
        f"size=600x400&"
        f"path=color:0x0000FF|weight:5|enc:{encoded_polyline}&"
        f"key={os.environ['GOOGLE_API_KEY']}"
    )

    response = requests.get(url)

    return response
