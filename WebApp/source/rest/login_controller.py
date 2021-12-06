from flask import Blueprint, Response

login_blueprint = Blueprint('login', __name__, template_folder='templates', url_prefix="/")


@login_blueprint.route('login', methods=['GET'])
async def get_login_form():
    return Response(status=200, mimetype="application/json")


@login_blueprint.route('register', methods=['GET'])
async def get_register_form():
    return Response(status=200, mimetype="application/json")


@login_blueprint.route('register', methods=['POST'])
async def register_user():
    return Response(status=200, mimetype="application/json")


@login_blueprint.route('login', methods=['POST'])
async def login_user():
    return Response(status=200, mimetype="application/json")
