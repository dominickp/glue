import pytest
import requests
from config import REQUEST_TIMEOUT, GLUE_IMPLEMENTATIONS


@pytest.mark.parametrize("host", GLUE_IMPLEMENTATIONS)
def test_get_index_browser(host):
    """
    Request the index page as a user with a browser. This should result in an HTML error response that tells the user
    to use `curl` instead.
    """
    url = f"{host}/"
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert "This API returns text-based responses intended to be used with curl." in response.text


@pytest.mark.parametrize("host", GLUE_IMPLEMENTATIONS)
def test_get_index_curl(host):
    """
    Request the index page as a user with curl. This should result in a text-based response that tells the user how to
    use the API.
    """
    url = f"{host}/"
    response = requests.get(url, headers={"User-Agent": "curl/7.79.1"}, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert "You should call /<board>/<page> to get the catalog of a board." in response.text
