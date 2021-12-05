import os

import aiohttp

from WebApp.app.modules.model.translation_request import TranslationRequest


async def translation_request(request):
    user_request = TranslationRequest().create_from_request(request)
    return await __make_request(user_request)


async def __make_request(user_request: TranslationRequest):
    SEND_IMAGE_FUNCTION_URL = os.getenv("UPLOAD_IMAGE_URL")
    form_data = __prepare_request_data(user_request)

    response = None
    async with aiohttp.ClientSession() as session:
        async with session.post(SEND_IMAGE_FUNCTION_URL, data=form_data) as session_response:
            response = await session_response.text()
    return response


def __prepare_request_data(user_request: TranslationRequest):
    form = aiohttp.FormData()
    form.add_field(name="email", value=user_request.email)
    form.add_field(name="language", value=user_request.language)
    form.add_field(name="", value=user_request.file.read(), content_type='image/jpeg')

    return form
