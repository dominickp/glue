/**
 * Returns a string representation of the threads for the given page number and board.
 * E.g.:
 *      Page 1
 *      - Welcome to /po/! (2)
 *      - No Stencil thread? What has happened to /po/ ? (1)
 *      - Bookbinding (36)
 *      ...
 * @param {Object} catalog - The catalog object
 * @param {number} pageNumber - The page number
 * @returns {string} - A string representation of the catalog for the given page number
 */
function getCLIFromCatalog(catalog, pageNumber = 1) {
  let cliResponse = `Page ${pageNumber}: \n`;
  const page = catalog[pageNumber - 1];
  for (const thread of page.threads) {
    let subject = thread.sub || thread.com || "No subject";
    subject = subject.length > 64 ? `${subject.substring(0, 64)}...` : subject;
    cliResponse += ` - ${subject} (${thread.replies} replies)\n`;
  }
  return cliResponse;
}

module.exports = { getCLIFromCatalog };
