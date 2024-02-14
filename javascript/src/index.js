const express = require("express");
const metrics = require("./metrics");
const chan = require("./chan_client");
const cli = require("./cli");
const app = express();
const port = 80;

/**
 * Middleware to start a timer for the request.
 */
app.use((req, res, next) => {
  res.locals.start = Date.now();
  next();
});

/**
 * Middleware to print access log
 */
app.use((req, res, next) => {
  console.log(
    `${req.ip} - - [${new Date().toUTCString()}] "${req.method} ${
      req.originalUrl
    } HTTP/${req.httpVersion}" ${res.statusCode}`
  );
  next();
});

/**
 * Middleware to handle CORS.
 */
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Methods", "*");
  res.header("Access-Control-Allow-Headers", "*");
  // Check for options request
  if (req.method === "OPTIONS") {
    res.sendStatus(204);
    metrics.captureResponseMetrics(req.method, req, res);
    return;
  }
  next();
});

/**
 * Middleware to check to ensure the request is coming from curl.
 */
app.use((req, res, next) => {
  // Bypass this check if prometheus is scraping /metrics
  if (req.path === "/metrics") {
    next();
    return;
  }
  const userAgent = req.get("User-Agent");
  if (userAgent && !userAgent.startsWith("curl")) {
    res.status(400).send(`<html>
        <div>
            <p>This API returns text-based responses intended to be used with curl.</p>
            <p>Try "curl %s".</p>
        </div>
    </html>`);
    metrics.captureResponseMetrics(req.method, req, res);
    return;
  }
  res.setHeader("content-type", "text/plain");
  next();
});

app.get("/", (req, res) => {
  res.send("You should call /<board>/<page> to get the catalog of a board.\n");
  metrics.captureResponseMetrics(req.method, req, res);
});

app.get("/metrics", async (req, res) => {
  res.set("Content-Type", metrics.register.contentType);
  res.end(await metrics.register.metrics());
});

app.get("/:board/:page?", async (req, res) => {
  const board = req.params.board;
  const page = req.params.page || 1;
  const client = new chan.ChanClient();
  try {
    // Forward along the x-forwarded-for header so the 4channel API knows the original IP of the user
    const fanoutHeaders = {
      "X-Forwarded-For": req.headers["x-forwarded-for"] || req.ip,
    };
    const catalog = await client.getCatalog(board, fanoutHeaders);
    const cliResponse = cli.getCLIFromCatalog(catalog, page);
    res.send(cliResponse);
    metrics.captureResponseMetrics(req.method, req, res);
    return;
  } catch (error) {
    if (error.name === "BadRequestError") {
      res.status(400).send(error.message);
      metrics.captureResponseMetrics(req.method, req, res);
      return;
    }
    res.status(500).send(error.message);
    metrics.captureResponseMetrics(req.method, req, res);
    return;
  }
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
