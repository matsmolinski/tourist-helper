import json
import os

import requests

from source.modules.common.status_dict import StatusDict
from source.modules.model.translation_request import TranslationRequest


async def translation_request(rq):
    user_request = TranslationRequest().create_from_request(rq)
    return await __make_request(user_request)


async def __make_request(user_request: TranslationRequest):
    # return StatusDict.REQUEST_SENT, None
    SEND_IMAGE_FUNCTION_URL = os.getenv("UPLOAD_IMAGE_URL")
    data, files = __prepare_request_data(user_request)

    response = requests.post(SEND_IMAGE_FUNCTION_URL, data=data, files=files)

    data = json.loads(response.text)
    if response.status_code in range(200, 300):
        return StatusDict.REQUEST_SENT, data
    else:
        return StatusDict.GENERAL_ERROR, data


def __prepare_request_data(user_request: TranslationRequest):
    data = {'email': user_request.email, 'language': user_request.language}
    files = [('', (f.filename, f.read())) for f in [user_request.file]]

    return data, files
