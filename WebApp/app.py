from flask import Flask
from dotenv import load_dotenv
from flask_session import Session

from source.rest.index_controller import index_blueprint
from source.rest.login_controller import login_blueprint
from source.rest.translations_controller import translations_blueprint

load_dotenv()
app = Flask(__name__)
app.secret_key = "SECRET KEY IN PLAIN TEXT PLZ DONT STEAL"

for blueprint in [translations_blueprint, login_blueprint, index_blueprint]:
    app.register_blueprint(blueprint)

server_session = Session(app)

#app.run()
