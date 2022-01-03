import json

from flask import Blueprint, render_template, Response, request, make_response, session

from source.modules.translations.translations import translation_request, fetch_translation_result

translations_blueprint = Blueprint('translation', __name__, template_folder='templates', url_prefix="/translation")


@translations_blueprint.route('', methods=['GET'])
async def get_translations_list():
    return render_template(template_name_or_list="translations_list.html")


@translations_blueprint.route('/details', methods=['GET'])
async def get_translation_details():
    status, data = await fetch_translation_result(request)
    return render_template(template_name_or_list="translations_details.html", original_text=data.original_text,
                           translation_text=data.translation_text, image_url = data.image_url)
    # return data


@translations_blueprint.route('/add-form', methods=['GET'])
async def get_translation_form():
    return render_template(template_name_or_list="translations_request.html")


@translations_blueprint.route('/add', methods=['POST'])
async def send_translation_request():
    status = await translation_request(request)
    return redirect(status)


def redirect(error_code, location="/"):
    response = make_response('', 303)
    session['error_code'] = str(error_code)
    response.headers["Location"] = location
    return response
