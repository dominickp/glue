from flask import Flask, request, Response, g
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from time import time
from flask_cors import CORS
from chan_client import ChanClient
from cli import get_cli_from_chan_catalog
from metrics import METRIC_TOTAL_REQUEST_TIME

app = Flask(__name__)
CORS(app)

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

@app.before_request
def before_request():
    """
    Check if the request is from curl. If not, return an HTML message to the user.
    """

    # Track the start time of the request to the flask object
    g.start = time()

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

@app.after_request
def after_request(response):
    """
    Capture the time spent on the request and record it as a metric.
    """
    # Calculate the total time spent on the request
    total_time = time() - g.start
    # Get the normalized route like "/<string:name>/<int:page>" if url_rule is present
    normalized_path = request.url_rule.rule if request.url_rule else "unmatched-route"
    # Ensure unmatched routes are recorded as "not_found"
    METRIC_TOTAL_REQUEST_TIME.labels(request.method, normalized_path, response.status_code).observe(total_time)
    return response

@app.route("/")
def index():
    response = Response("You should call /<board>/<page> to get the catalog of a board.\n")
    response.mimetype = "text/plain"
    return response

@app.route("/<string:name>")
@app.route("/<string:name>/<int:page>")
def list_threads(name, page=1):
    chan = ChanClient()
    # Forward along the x-forwarded-for header so the 4channel API knows the original IP of the user
    headers = {"x-forwarded-for": request.headers.get("x-forwarded-for", request.remote_addr)}
    try:
        catalog = chan.get_catalog(name, headers)
        response = Response(get_cli_from_chan_catalog(catalog, page))
    except ValueError as e:
        response = Response(str(e))
        response.status_code = 400
    except Exception as e:
        response = Response(str(e))
        response.status_code = 500
    response.mimetype = "text/plain"
    return response
