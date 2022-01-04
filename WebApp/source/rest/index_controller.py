from flask import Blueprint, render_template, session

from source.rest.common import create_error_message_fragment, redirect

index_blueprint = Blueprint('index', __name__, template_folder='templates', url_prefix="/")


@index_blueprint.route('', methods=['GET'])
async def get_index():
    message = create_error_message_fragment(session.pop("error_code", None))
    return render_template(template_name_or_list="index.html", message=message)

