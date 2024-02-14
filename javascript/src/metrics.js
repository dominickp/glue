const client = require("prom-client");
// Setup metrics
const collectDefaultMetrics = client.collectDefaultMetrics;
const register = new client.Registry();
register.setDefaultLabels({ app: "glue-js" });
collectDefaultMetrics({ register });

// prettier-ignore
ms_buckets = [
    5, 10, 25, 50, 75, 100, 125 ,150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 600, 
    700, 800, 900, 1000, 2000, 3000, 4000, 5000, "+Inf"
]

// Define custom metrics
const METRIC_TOTAL_REQUEST_TIME = new client.Histogram({
  name: "request_time_seconds",
  help: "Time spent making requests to the service",
  labelNames: ["method", "endpoint", "response_code"],
  buckets: ms_buckets,
});
register.registerMetric(METRIC_TOTAL_REQUEST_TIME);

const METRIC_FANOUT_REQUEST_TIME = new client.Histogram({
  name: "fanout_request_time_seconds",
  help: "Time spent processing fanout requests",
  labelNames: ["method", "endpoint", "response_code"],
  buckets: ms_buckets,
});
register.registerMetric(METRIC_FANOUT_REQUEST_TIME);

const METRIC_CHAN_BOARDS_REQUESTED = new client.Counter({
  name: "chan_boards_requested",
  help: "Number of times a 4channel board was requested",
  // I'm not including the page number because it's not a bounded set
  labelNames: ["board"], // e.g. "po"
});
register.registerMetric(METRIC_CHAN_BOARDS_REQUESTED);

/**
 * Capture response metrics for the given request.
 * @param {string} method - The HTTP method of the request.
 * @param {string} endpoint - The endpoint of the request.
 * @param {Object} response - The response object.
 */
const captureResponseMetrics = (method, request, response) => {
  const start = response.locals.start;
  const responseTimeInMilliseconds = Date.now() - start;
  // Get the normalized route like "/<string:name>/<int:page>" if url_rule is present
  // Ensure unmatched routes are recorded as "not_found"
  const endpoint = request.route ? request.route.path : "not_found";
  return METRIC_TOTAL_REQUEST_TIME.observe(
    { method, endpoint: endpoint, response_code: response.statusCode },
    responseTimeInMilliseconds
  );
};

module.exports = {
  register,
  METRIC_CHAN_BOARDS_REQUESTED,
  METRIC_FANOUT_REQUEST_TIME,
  METRIC_TOTAL_REQUEST_TIME,
  captureResponseMetrics,
};
