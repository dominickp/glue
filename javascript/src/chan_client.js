const metrics = require("./metrics");

const REQUEST_TIMEOUT = 5;
const DEFAULT_CHAN_HOST = "https://a.4cdn.org";
const CHAN_HOST = process.env.CHAN_HOST || DEFAULT_CHAN_HOST;
const SFW_4CHAN_BOARDS = ["po", "g", "fa", "mu", "v"];

class BadRequestError extends Error {
  constructor(message) {
    super(message);
    this.name = "BadRequestError";
  }
}

class ChanClient {
  constructor(host = CHAN_HOST) {
    this.host = host;
  }

  /**
   * Handle HTTP requests and capture metrics.
   * @param {string} method - The HTTP method to use (e.g. "GET").
   * @param {string} url - The URL to request.
   * @param {Object} headers - Optional headers to include in the request.
   * @returns {Promise} - A promise that resolves with the response.
   */
  async handleRequest(method, url, headers = {}) {
    const start = Date.now();
    const response = await fetch(url, {
      method: method,
      signal: AbortSignal.timeout(REQUEST_TIMEOUT * 1000),
      headers: headers,
    });
    const end = Date.now();
    const elapsed = end - start;
    metrics.METRIC_FANOUT_REQUEST_TIME.observe(
      { method: method, endpoint: url, response_code: response.status },
      elapsed
    );
    return response;
  }

  /**
   * Get the catalog of a supported SFW board.
   * @param {string} board - The board to get the catalog of (e.g. "po" for Papercraft & Origami).
   * @param {Object} headers - Optional headers to include in the request.
   * @returns {Promise} - A promise that resolves with the catalog
   */
  async getCatalog(board, headers = {}) {
    if (!board) {
      throw new BadRequestError("Board is required.");
    }
    if (!SFW_4CHAN_BOARDS.includes(board)) {
      throw new BadRequestError(`Board ${board} is not a supported SFW board.`);
    }

    // Capture the 4channel board metric now that we know the value is of a small set.
    metrics.METRIC_CHAN_BOARDS_REQUESTED.inc({ board: board });

    const url = `${this.host}/${board}/catalog.json`;
    const response = await this.handleRequest("GET", url, headers);
    if (!response.ok) {
      throw new Error(`Failed to fetch catalog for board ${board}.`);
    }
    return response.json();
  }
}

module.exports = { ChanClient };
