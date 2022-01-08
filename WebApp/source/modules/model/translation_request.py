import uuid
from dataclasses import dataclass

from flask import Request
from werkzeug.datastructures import FileStorage


@dataclass
class TranslationRequest:
    email: str
    language: str
    file: FileStorage
    registered_user: bool
    token: str

    @classmethod
    def create_from_request(cls, request: Request, email: str):
        email = request.form.get("email", None) if request.form.get("email", None) is not None else email
        language = request.form.get("language", None)
        file = request.files.get("file", None)
        registered_user = True if request.form.get("email", None) is None else False
        token = uuid.uuid4().hex
        return TranslationRequest(email, language, file, registered_user, token)
