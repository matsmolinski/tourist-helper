from flask import Flask

from source.rest.index import index_blueprint


app = Flask(__name__)
app.register_blueprint(
    index_blueprint
)
