from flask import Blueprint, render_template

index_blueprint = Blueprint('index_page', __name__, template_folder='templates', url_prefix="/")


@index_blueprint.route('', methods=['GET'])
async def index():
    # session_id = request.cookies.get('session_id')
    # session_id = response.set_cookie("session_id", session_id, max_age=INVALIDATE, httponly=True, secure=True,
    #                                 samesite='Strict')
    # TODO dekorator pod sprawdzanie sesji

    return render_template(template_name_or_list="index.html", uid="twój stary", listToken=["example", "list", "of", "things"],
                           listOfPublications={"smok": "smok",
                                               "kot": "kot",
                                               "pies": "pies",
                                               "lama": "lama"}, message="abc")

