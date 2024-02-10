const express = require("express");
const chan = require("./chan_client");
const cli = require("./cli");
const app = express();
const port = 3000;

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
    return;
  }
  next();
});

/**
 * Middleware to check to ensure the request is coming from curl.
 */
app.use((req, res, next) => {
  const userAgent = req.get("User-Agent");
  if (userAgent && !userAgent.startsWith("curl")) {
    res.status(400).send(`<html>
        <div>
            <p>This API returns text-based responses intended to be used with curl.</p>
            <p>Try "curl %s".</p>
        </div>
    </html>`);
    return;
  }
  res.setHeader("content-type", "text/plain");
  next();
});

app.get("/", (req, res) => {
  res.send("You should call /<board>/<page> to get the catalog of a board.\n");
});

app.get("/:board/:page?", async (req, res) => {
  const board = req.params.board;
  const page = req.params.page || 1;
  const client = new chan.ChanClient();
  try {
    const catalog = await client.getCatalog(board);
    const cliResponse = cli.getCLIFromCatalog(catalog, page);
    res.send(cliResponse);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
