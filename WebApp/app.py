from flask import Flask
from dotenv import load_dotenv

from WebApp.app.rest.index_controller import index_blueprint
from WebApp.app.rest.login_controller import login_blueprint
from WebApp.app.rest.translations_controller import translations_blueprint


if __name__ == "__main__":
    load_dotenv()
    app = Flask(__name__)

    for blueprint in [translations_blueprint, login_blueprint, index_blueprint]:
        app.register_blueprint(blueprint)

    app.run(host="localhost", port=5005)
