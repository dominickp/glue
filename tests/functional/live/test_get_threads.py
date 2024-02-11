
import pytest
import requests
from config import REQUEST_TIMEOUT, GLUE_IMPLEMENTATIONS


@pytest.mark.parametrize("host", GLUE_IMPLEMENTATIONS)
def test_get_threads_curl_page_1(host):
    """
    Request the page 1 of /po/ as a user with curl. This fans out the live 4channel API.
    """
    url = f"{host}/po/1"
    response = requests.get(url, headers={"User-Agent": "curl/7.79.1"}, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert response.text.startswith("Page 1")
    # Ensure the response is long enough to contain the expected number of threads. It should be 16 per page, so 17 
    # lines. But we'll be lenient and just check for more than 10 so this isn't so brittle.
    assert len(response.text.split("\n")) > 10
