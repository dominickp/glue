from prometheus_client import start_http_server, Histogram
import time

# Create a metric to track time spent and requests made.
ms_buckets = [
    25, 50, 75, 100, 125 ,150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 600, 
    700, 800, 900, 1000, 2000, 3000, 4000, 5000, "+Inf"
]
METRIC_TOTAL_REQUEST_TIME = Histogram(
    "total_request_seconds", 
    "Time spent making requests to the service", 
    ["method", "endpoint", "response_code"],
    buckets=ms_buckets
)
METRIC_FANOUT_REQUEST_TIME = Histogram(
    "fanout_request_seconds", 
    "Time spent processing fanout requests", 
    ["method", "endpoint", "response_code"],
    buckets=ms_buckets
)


