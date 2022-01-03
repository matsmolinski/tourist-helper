import json
import os

import requests

from source.modules.common.status_dict import StatusDict
from source.modules.model.translation_request import TranslationRequest
from source.modules.model.translation_response import TranslationResponse


async def fetch_translation_result(rq):
    token = rq.args.get("token", None)
    return await __fetch_result(token)


async def __fetch_result(token):
    FETCH_TRANSLATION_URL = os.getenv("FETCH_TRANSLATION_URL")
    response = requests.get(FETCH_TRANSLATION_URL, data={"token": token})

    if response.status_code in range(200, 300):
        json_response = response.json()[0]

        translation_text = json_response['translation']
        translation_text = translation_text.replace("\\n", " ").split(":")[2][:-1]

        original_text = json_response['image_text']
        original_text = original_text.replace("\n", " ")

        file_path = f'{os.getenv("PHOTO_CONTAINER_URL")}/{json_response["RowKey"]}.{json_response["PartitionKey"]}'

        data = TranslationResponse(original_text, translation_text, file_path)

        return StatusDict.TRANSLATION_FETCHED, data
    else:
        return StatusDict.GENERAL_ERROR, None


async def translation_request(rq):
    user_request = TranslationRequest().create_from_request(rq)
    return await __make_request(user_request)


async def __make_request(user_request: TranslationRequest):
    # return StatusDict.REQUEST_SENT, None
    SEND_IMAGE_FUNCTION_URL = os.getenv("UPLOAD_IMAGE_URL")
    data, files = __prepare_request_data(user_request)

    response = requests.post(SEND_IMAGE_FUNCTION_URL, data=data, files=files)

    if response.status_code in range(200, 300):
        return StatusDict.REQUEST_SENT
    else:
        return StatusDict.GENERAL_ERROR


def __prepare_request_data(user_request: TranslationRequest):
    data = {'email': user_request.email, 'language': user_request.language}
    files = [('', (f.filename, f.read())) for f in [user_request.file]]

    return data, files
