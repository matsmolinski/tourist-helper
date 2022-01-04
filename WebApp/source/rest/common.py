from flask import make_response, session

from source.modules.common.status_dict import StatusDict


def create_error_message_fragment(error_code):
    if StatusDict.REQUEST_SENT == error_code:
        return f'<div class="info">Translation request has been sent!</div>'
    elif StatusDict.GENERAL_ERROR == error_code:
        return f'<div class="error">Error has occurred!</div>'
    return ''


def redirect(error_code, location="/"):
    response = make_response('', 303)
    session['error_code'] = str(error_code)
    response.headers["Location"] = location
    return response
