import json
import os
from typing import List

import requests
from redis import StrictRedis

from source.modules.common.redis_connection import get_redis
from source.modules.common.status_dict import StatusDict, TranslationStatusDict
from source.modules.model.translation_request import TranslationRequest
from source.modules.model.translation_response import TranslationResponse, TranslationListEntry


async def fetch_translations_list(email: str):
    tokens = await __fetch_user_tokens(email)

    FETCH_TRANSLATION_URL = os.getenv("FETCH_TRANSLATION_URL")
    entries = []

    with requests.Session() as session:
        for token in tokens:
            response = session.get(f'{FETCH_TRANSLATION_URL}', data={"token": token})
            if response.status_code in range(200, 300):
                json_response = response.json()[0]
                entries.append(
                    TranslationListEntry(json_response['Timestamp'][:-13],
                                         TranslationStatusDict.READY.value if json_response[
                                             'image_text'] else TranslationStatusDict.IN_PROGRESS.value,
                                         f'{os.getenv("PHOTO_CONTAINER_URL")}/{json_response["RowKey"]}.{json_response["PartitionKey"]}',
                                         json_response['token']))

    return entries


async def fetch_translation_result(rq):
    token = rq.args.get("token", None)
    return await __fetch_result(token)


async def translation_request(rq, email: str):
    user_request = TranslationRequest.create_from_request(rq, email)
    return await __make_request(user_request)


async def __fetch_user_tokens(email: str):
    redis: StrictRedis = get_redis()
    user_tokens = json.loads(redis.hget("user_tokens", email).decode("UTF-8"))
    return user_tokens


async def __save_user_tokens(email: str, tokens: List[str]):
    redis: StrictRedis = get_redis()
    redis.hset("user_tokens", email, json.dumps(tokens))


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


async def __make_request(user_request: TranslationRequest):
    SEND_IMAGE_FUNCTION_URL = os.getenv("UPLOAD_IMAGE_URL")
    data, files = __prepare_request_data(user_request)

    response = requests.post(SEND_IMAGE_FUNCTION_URL, data=data, files=files)

    if response.status_code in range(200, 300):
        if user_request.registered_user:
            tokens = await __fetch_user_tokens(user_request.email)
            tokens.append(user_request.token)
            await __save_user_tokens(user_request.email, tokens)
        return StatusDict.REQUEST_SENT
    else:
        return StatusDict.GENERAL_ERROR


def __prepare_request_data(user_request: TranslationRequest):
    data = {'email': user_request.email, 'language': user_request.language, 'token': user_request.token}
    files = [('', (f.filename, f.read())) for f in [user_request.file]]

    return data, files
