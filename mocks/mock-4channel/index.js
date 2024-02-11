const express = require("express");
const fs = require("fs");
const app = express();
const port = 3000;

const jsonFilePath = "/app/json";

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
