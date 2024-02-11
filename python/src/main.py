from flask import Flask, request, Response
from flask_cors import CORS
from chan_client import ChanClient
from cli import get_cli_from_chan_catalog

app = Flask(__name__)
CORS(app)


@app.before_request
def before_request():
    """
    Check if the request is from curl. If not, return an HTML message to the user.
    """
    # Allow CORS preflight requests
    if request.method.lower() == "options":
        return "", 204
    # If the request is not from curl, return an HTML message
    if "curl" not in request.headers.get("User-Agent", ""):
        return f"""<div>
            <p>This API returns text-based responses intended to be used with curl.</p>
            <p>Try \"curl {request.url}\".</p>
        </div>""", 400
    pass

@app.route("/")
def index():
    response = Response("You should call /<board>/<page> to get the catalog of a board.\n")
    response.mimetype = "text/plain"
    return response

@app.route("/<string:name>")
@app.route("/<string:name>/<int:page>")
def list_threads(name, page=1):
    chan = ChanClient()
    catalog = chan.get_catalog(name)
    response = Response(get_cli_from_chan_catalog(catalog, page))
    response.mimetype = "text/plain"
    return response
