from flask import Flask

from WebApp.app.rest.index import index_blueprint


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(
        index_blueprint
    )
    app.run(host="localhost", port=5005)
