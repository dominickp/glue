const express = require("express");
const fs = require("fs");
const app = express();
const port = 80;

const jsonFilePath = "/app/json";

// Helper function to check for comma seperated values in the x-forwarded-for header
// The x-forward-for might have a value like "4c-mock-delay=1,4c-mock-status-code=500"
// Would return the value of 1 if called for "4c-mock-delay" and 500 if called for "4c-mock-status-code"
function getXFFSignal(req, target) {
  const xff = req.get("x-forwarded-for");
  if (!xff) {
    return null;
  }
  const signals = xff.split(",");
  for (const signal of signals) {
    const [key, value] = signal.split("=");
    if (key === target) {
      return value;
    }
  }
  return null;
}

/** Middleware to check for generic signals */
app.use((req, res, next) => {
  const delay = getXFFSignal(req, "4c-mock-delay");
  const statusCode = getXFFSignal(req, "4c-mock-status-code");
  if (delay) {
    console.log(`Delaying response by ${delay} seconds`);
    setTimeout(() => {
      next();
    }, delay * 1000);
  } else if (statusCode) {
    console.log(`Returning mock status code ${statusCode}`);
    return res.sendStatus(statusCode);
  } else {
    next();
  }
});

app.get("/", (req, res) => {
  res.send("Welcome to mock-4channel.");
});

app.get("/:board/:file", (req, res) => {
  const board = req.params.board;
  const file = req.params.file;

  // Load JSON file async from disk
  const targetFile = `${jsonFilePath}/${board}/${file}`;
  fs.readFile(targetFile, (err, data) => {
    if (err) {
      res.status(404).send(`File "${targetFile}" not found`);
      return;
    }
    res.setHeader("Content-Type", "application/json");
    return res.send(data);
  });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
