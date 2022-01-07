from flask import make_response, session

from source.modules.common.status_dict import StatusDict


def create_error_message_fragment(error_code):
    if StatusDict.REQUEST_SENT == error_code:
        return f'<div class="info">Translation request has been sent!</div>'
    elif StatusDict.GENERAL_ERROR == error_code:
        return f'<div class="error">Error has occurred!</div>'
    elif StatusDict.INCORRECT_CREDENTIALS == error_code:
        return f'<div class="error">Incorrect credentials!</div>'
    elif StatusDict.LOGGED_OUT == error_code:
        return f'<div class="info">Logged out successfully!</div>'
    return ''


def redirect(error_code, location="/"):
    response = make_response('', 303)
    session['error_code'] = str(error_code)
    response.headers["Location"] = location
    return response


def logged_only(error_code=StatusDict.INCORRECT_CREDENTIALS.value, redirection_url="/"):
    def inner(func):
        def wrapper(*args, **kwargs):
            if session.get('email', None) is not None:
                func(*args, **kwargs)
            else:
                redirect(error_code, redirection_url)
        return wrapper
    return inner


def redirect_if_logged(redirection_url="/translation"):
    def inner(func):
        def wrapper(*args, **kwargs):
            if session.get('email', None) is None:
                func(*args, **kwargs)
            else:
                redirect(None, redirection_url)
        return wrapper
    return inner
