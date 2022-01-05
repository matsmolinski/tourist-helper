from dataclasses import dataclass

from flask import Request
from werkzeug.datastructures import FileStorage


@dataclass
class TranslationRequest:
    email: str
    language: str
    file: FileStorage

    @classmethod
    def create_from_request(cls, request: Request):
        email = request.form.get("email", None)
        language = request.form.get("language", None)
        file = request.files.get("file", None)
        return TranslationRequest(email, language, file)
