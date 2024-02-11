import os
import requests
import logging
from furl import furl

REQUEST_TIMEOUT = 5
DEFAULT_CHAN_HOST = "https://a.4cdn.org"
CHAN_HOST = os.environ.get("CHAN_HOST", DEFAULT_CHAN_HOST)

SFW_4CHAN_BOARDS = frozenset(["po", "g", "fa", "mu", "v"])

class ChanClient:
    def __init__(self, host=CHAN_HOST):
        self.host = host

    def get_catalog(self, board, headers={}):
        """
        Get the catalog of a supported SFW board.
        :param board: The board to get the catalog of (e.g. "po" for Papercraft & Origami).
        :param headers: Optional headers to send with the request.
        """
        if not board:
            raise ValueError("Board cannot be empty.")
        if board not in SFW_4CHAN_BOARDS:
            raise ValueError(f"Board {board} is not a supported SFW board.")
        
        # Example: https://a.4cdn.org/po/catalog.json
        url = furl(CHAN_HOST).add(path=[board, "catalog.json"]).url

        chan_r = requests.get(url, timeout=REQUEST_TIMEOUT, headers=headers)
        if not chan_r:
            logging.error(f"Failed to get catalog for board {board}.")
            raise Exception(f"Failed to get catalog for board {board}.")

        return chan_r.json()
