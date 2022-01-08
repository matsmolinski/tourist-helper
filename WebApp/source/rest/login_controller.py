from flask import Blueprint, render_template, request, session

from source.modules.auth.auth_manager import authenticate_user, register_new_user
from source.modules.common.status_dict import StatusDict
from source.rest.common import redirect, redirect_if_logged, logged_only, create_error_message_fragment

login_blueprint = Blueprint('login', __name__, template_folder='templates', url_prefix="/")


@login_blueprint.route('login', methods=['GET'])
@redirect_if_logged()
async def get_login_form():
    message = create_error_message_fragment(session.pop("error_code", None))
    return render_template(template_name_or_list="login_form.html", message=message)


@login_blueprint.route('register', methods=['GET'])
@redirect_if_logged()
async def get_register_form():
    message = create_error_message_fragment(session.pop("error_code", None))
    return render_template(template_name_or_list="register_form.html", message=message)


@login_blueprint.route('register', methods=['POST'])
@redirect_if_logged()
async def register_user():
    form_args = request.form
    status = register_new_user(form_args)
    if status == StatusDict.ACCOUNT_CREATED:
        route = "/"
    else:
        route = "/register"
    return redirect(status, route)


@login_blueprint.route('login', methods=['POST'])
@redirect_if_logged()
async def login_user():
    form_args = request.form
    if authenticate_user(form_args):
        session['email'] = form_args.get('email')
        return redirect(None, "/translation")
    else:
        return redirect(StatusDict.INCORRECT_CREDENTIALS, "/login")


@login_blueprint.route('logout', methods=['GET'])
@logged_only(error_code=None)
async def logout_user():
    session.pop('email', None)
    return redirect(StatusDict.LOGGED_OUT, "/")
