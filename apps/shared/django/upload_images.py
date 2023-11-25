import httpx

url = 'https://telegra.ph/upload'


def upload_image(image) -> str:
    response, success = upload_image_server(image)
    url = 'https://telegra.ph'
    if success:
        return url + response[0]['src']
    else:
        raise 'uploading image error'


def upload_image_server(image) -> tuple:
    response = httpx.post(url, files={'file': image})
    if response.status_code == 200:
        return response.json(), True

    return response.text, False
