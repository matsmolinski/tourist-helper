import os

import requests

from source.modules.common.status_dict import StatusDict, TranslationStatusDict
from source.modules.model.translation_request import TranslationRequest
from source.modules.model.translation_response import TranslationResponse, TranslationListEntry


async def fetch_translations_list():
    tokens = [
        "9f7eec06-ddcc-4572-90d5-f8d142170f45",
        "97908544-20a2-49e8-9d97-007b16db689b",
        "ce5ec719-9b01-40f5-9541-d55e3c0ef352",
        "803dee61-986e-4bce-8311-8baff340f3ef"
    ]

    FETCH_TRANSLATION_URL = os.getenv("FETCH_TRANSLATION_URL")
    entries = []

    with requests.Session() as session:
        for token in tokens:
            response = session.get(f'{FETCH_TRANSLATION_URL}', data={"token": token})
            if response.status_code in range(200, 300):
                json_response = response.json()[0]
                entries.append(
                    TranslationListEntry(json_response['Timestamp'][:-13], TranslationStatusDict.READY.value if json_response[
                        'image_text'] else TranslationStatusDict.IN_PROGRESS.value,
                                         f'{os.getenv("PHOTO_CONTAINER_URL")}/{json_response["RowKey"]}.{json_response["PartitionKey"]}', json_response['token']))

    return entries


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
    user_request = TranslationRequest.create_from_request(rq)
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
