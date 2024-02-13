import os
import requests
import logging
from time import time
from furl import furl
from metrics import METRIC_FANOUT_REQUEST_TIME

REQUEST_TIMEOUT = 5
DEFAULT_CHAN_HOST = "https://a.4cdn.org"
CHAN_HOST = os.environ.get("CHAN_HOST", DEFAULT_CHAN_HOST)

SFW_4CHAN_BOARDS = frozenset(["po", "g", "fa", "mu", "v"])

class ChanClient:
    def __init__(self, host=CHAN_HOST):
        self.host = host
    
    def handle_request(self, method, url, headers={}):
        """
        Make a request and record the time spent on the request.
        :param method: The HTTP method to use (e.g. "GET").
        :param url: The URL to request.
        :param headers: Optional headers to send with the request.
        """
        start = time()
        chan_r = requests.request(method, url, timeout=REQUEST_TIMEOUT, headers=headers)
        total_time = time() - start
        METRIC_FANOUT_REQUEST_TIME.labels(method, url, chan_r.status_code).observe(total_time)
        return chan_r

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

        chan_r = self.handle_request("GET", url, headers)
        if not chan_r:
            logging.error(f"Failed to get catalog for board {board}.")
            raise Exception(f"Failed to get catalog for board {board}.")

        return chan_r.json()
