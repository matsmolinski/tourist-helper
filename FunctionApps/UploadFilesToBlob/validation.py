import logging
import re

from UploadFilesToBlob.common import create_message

MISSING_FILE = "Missing file in for-data body"
MISSING_EMAIL = "Missing email in request body"
INVALID_EMAIL = "Invaild email format"

__logger = logging.getLogger('validation')


def validate_request(req):
    return [__validate_data(req), __validate_files(req)]


def __validate_data(req):
    req_keys = req.form.keys()

    if 'email' not in req_keys:
        logging.error(MISSING_EMAIL)
        return create_message(MISSING_EMAIL)

    email = req.form.get('email')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        logging.error(INVALID_EMAIL)
        return create_message(INVALID_EMAIL)


def __validate_files(req):
    files_number = len(req.files.to_dict().items())

    if files_number == 0:
        logging.error(MISSING_FILE)
        return create_message(MISSING_FILE)



