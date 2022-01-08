from pathlib import Path

from flask import Flask
from dotenv import load_dotenv

from source.rest.index_controller import index_blueprint
from source.rest.login_controller import login_blueprint
from source.rest.translations_controller import translations_blueprint

dotenv_path = Path("setting.yaml")
load_dotenv(dotenv_path=dotenv_path)
app = Flask(__name__)
app.secret_key = "SECRET KEY IN PLAIN TEXT PLZ DONT STEAL"

for blueprint in [translations_blueprint, login_blueprint, index_blueprint]:
    app.register_blueprint(blueprint)

# app.run()
