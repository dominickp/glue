from flask import Flask, request
from chan_client import ChanClient
from cli import get_cli_from_chan_catalog

app = Flask(__name__)

@app.before_request
def before_request():
    if "curl" not in request.headers.get("User-Agent", ""):
        return f"This API returns text-based responses intended to be used with curl. Try \"curl {request.url}\".", 400
    pass

@app.route("/")
def index():
    return "You should call /<board>/<page> to get the catalog of a board.\n"

@app.route("/<string:name>")
@app.route("/<string:name>/<int:page>")
def list_threads(name, page=1):
    chan = ChanClient()
    catalog = chan.get_catalog(name)
    return get_cli_from_chan_catalog(catalog, page)
