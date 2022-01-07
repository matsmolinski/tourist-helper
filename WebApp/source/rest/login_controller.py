from flask import Blueprint, Response, render_template, request, session

from source.modules.auth.auth_manager import authenticate_user
from source.modules.common.status_dict import StatusDict
from source.rest.common import redirect, redirect_if_logged, logged_only

login_blueprint = Blueprint('login', __name__, template_folder='templates', url_prefix="/")


@redirect_if_logged()
@login_blueprint.route('login', methods=['GET'])
async def get_login_form():
    return render_template(template_name_or_list="login.html")


@redirect_if_logged()
@login_blueprint.route('register', methods=['GET'])
async def get_register_form():
    return Response(status=200, mimetype="application/json")


@redirect_if_logged()
@login_blueprint.route('register', methods=['POST'])
async def register_user():
    return Response(status=200, mimetype="application/json")


@redirect_if_logged()
@login_blueprint.route('login', methods=['POST'])
async def login_user():
    form_args = request.form
    if authenticate_user(form_args):
        session['email'] = form_args.get('email')
        redirect("/translations")
    else:
        redirect("/login", StatusDict.INCORRECT_CREDENTIALS)
    return Response(status=200, mimetype="application/json")


@logged_only(error_code=None)
@login_blueprint.route('logout', methods=['GET'])
async def logout_user():
    session.pop('email', None)
    redirect("/", StatusDict.LOGGED_OUT)
