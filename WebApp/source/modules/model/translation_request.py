from flask import Request
from werkzeug.datastructures import FileStorage


class TranslationRequest:
    email: str
    language: str
    file: FileStorage

    @classmethod
    def create_from_request(cls, request: Request):
        obj = cls()
        obj.email = request.form.get("email", None)
        obj.language = request.form.get("language", None)
        obj.file = request.files.get("file", None)
        return obj
