import httpx

from django.core.files.uploadhandler import UploadFileException

url = 'https://telegra.ph/upload'


def upload_image(instance, filename):
    response, success = upload_image_server(instance.image)

    if success:
        return url + response[0]['src']
    else:
        raise UploadFileException(response)


def upload_image_server(image):
    response = httpx.post(url, files={'file': image})
    if response.status_code == 200:
        return response.json(), True

    return response.text, False
