from source.modules.common.status_dict import StatusDict


def create_error_message_fragment(error_code):
    if StatusDict.REQUEST_SENT == error_code:
        return f'<div class="info">Translation request has been sent!</div>'
    elif StatusDict.GENERAL_ERROR == error_code:
        return f'<div class="error">Error has occurred!</div>'
    return ''
