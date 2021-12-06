from flask import Blueprint, render_template, Response, request
import json
from source.modules.translations.translations import translation_request

translations_blueprint = Blueprint('translation', __name__, template_folder='templates', url_prefix="/translation")


@translations_blueprint.route('', methods=['GET'])
async def get_translations_list():
    return render_template(template_name_or_list="translations_list.html")


@translations_blueprint.route('', methods=['GET'])
async def get_translation_details():
    return Response(status=200, mimetype="application/json")


@translations_blueprint.route('', methods=['GET'])
async def get_translation_form():
    return Response(status=200, mimetype="application/json")


@translations_blueprint.route('', methods=['POST'])
async def send_translation_request():
    status = await translation_request(request)
    return Response(status=200, mimetype="application/json", response=json.dumps({"function_app_status": status}))
