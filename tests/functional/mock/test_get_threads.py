import pytest
import requests
from config import REQUEST_TIMEOUT, GLUE_IMPLEMENTATIONS


@pytest.mark.parametrize("host", GLUE_IMPLEMENTATIONS)
def test_get_threads_browser(host):
    """
    Request the threads page as a user with a browser. This should result in an HTML error response that tells the user
    to use `curl` instead.
    """
    url = f"{host}/po/1"
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert "This API returns text-based responses intended to be used with curl." in response.text


@pytest.mark.parametrize("host", GLUE_IMPLEMENTATIONS)
def test_get_threads_curl_page_1(host):
    """
    Request the page 1 of /po/ as a user with curl. This page is mocked out to return 4 threads, each with the subject
    present.
    """
    url = f"{host}/po/1"
    response = requests.get(url, headers={"User-Agent": "curl/7.79.1"}, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert response.text == \
"""Page 1: 
 - Subject 1 (10 replies)
 - Subject 2 (10 replies)
 - Subject 3 (10 replies)
 - Subject 4 (0 replies)
"""

@pytest.mark.parametrize("host", GLUE_IMPLEMENTATIONS)
def test_get_threads_curl_page_2(host):
    """
    Request the page 2 of /po/ as a user with curl. Each thread (except the last) has either a missing or null subject, 
    so this test proves that the application falls back to the comment when the subject is missing.
    """
    url = f"{host}/po/2"
    response = requests.get(url, headers={"User-Agent": "curl/7.79.1"}, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert response.text == \
"""Page 2: 
 - Comment 1 (10 replies)
 - Comment 2 (10 replies)
 - Comment 3 (10 replies)
 - Subject 4 (10 replies)
"""

@pytest.mark.parametrize("host", GLUE_IMPLEMENTATIONS)
def test_get_threads_curl_page_3(host):
    """
    Request the page 3 of /po/ as a user with curl. The first thread has a long subject, the second only has a long
    comment. This test proves that the truncation of the subject works as expected.
    """
    url = f"{host}/po/3"
    response = requests.get(url, headers={"User-Agent": "curl/7.79.1"}, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert response.text == \
"""Page 3: 
 - Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque... (10 replies)
 - Vestibulum faucibus semper lacus a sagittis. Suspendisse egestas... (10 replies)
"""
