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
    const url = `${this.host}/${board}/catalog.json`;
    const response = await fetch(url, {
      method: "GET",
      timeout: REQUEST_TIMEOUT,
      headers: headers,
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch catalog for board ${board}.`);
    }
    return response.json();
  }
}

module.exports = { ChanClient };
