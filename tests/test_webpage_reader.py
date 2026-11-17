import requests

from tools import webpage_reader


def test_extract_webpage_rejects_empty_url():
    result = webpage_reader.extract_webpage("")
    assert result == "Error: URL cannot be empty."


def test_extract_webpage_success(monkeypatch):
    class MockResponse:
        status_code = 200
        headers = {"Content-Type": "text/html"}
        text = "<html><body>Example content</body></html>"

        def raise_for_status(self):
            pass

    monkeypatch.setattr(
        webpage_reader.requests,
        "get",
        lambda *args, **kwargs: MockResponse()
    )
    monkeypatch.setattr(
        webpage_reader.trafilatura,
        "extract",
        lambda *args, **kwargs: "Example webpage content"
    )

    result = webpage_reader.extract_webpage("https://example.com")

    assert "Source URL: https://example.com" in result
    assert "HTTP Status: 200" in result
    assert "Example webpage content" in result


def test_extract_webpage_handles_request_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Connection timed out")

    monkeypatch.setattr(webpage_reader.requests, "get", mock_get)

    result = webpage_reader.extract_webpage("https://example.com")

    assert "Webpage request failed" in result
    assert "Connection timed out" in result


def test_extract_webpage_handles_empty_extraction(monkeypatch):
    class MockResponse:
        status_code = 200
        headers = {"Content-Type": "text/html"}
        text = "<html></html>"

        def raise_for_status(self):
            pass

    monkeypatch.setattr(
        webpage_reader.requests,
        "get",
        lambda *args, **kwargs: MockResponse()
    )
    monkeypatch.setattr(
        webpage_reader.trafilatura,
        "extract",
        lambda *args, **kwargs: None
    )

    result = webpage_reader.extract_webpage("https://example.com")

    assert "Could not extract readable content" in result
import pytest

from tools.webpage_reader import validate_url


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com",
        "http://example.org/page"
    ]
)
def test_validate_url_accepts_public_http_urls(url):
    assert validate_url(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.com",
        "file:///C:/Windows/win.ini",
        "http://localhost",
        "http://127.0.0.1",
        "http://192.168.1.1",
        "http://10.0.0.1",
        "http://169.254.1.1",
        "https://user:password@example.com"
    ]
)
def test_validate_url_rejects_unsafe_urls(url):
    assert validate_url(url) is False

def test_extract_webpage_allows_valid_redirect(monkeypatch):
    class MockResponse:
        def __init__(self, status_code, headers=None):
            self.status_code = status_code
            self.headers = headers or {}
            self.text = "<html>Example</html>"

        def raise_for_status(self):
            pass

    responses = [
        MockResponse(302, {"Location": "https://example.org/page"}),
        MockResponse(200, {"Content-Type": "text/html"})
    ]

    calls = []

    def mock_get(url, **kwargs):
        calls.append(url)
        return responses.pop(0)

    monkeypatch.setattr(webpage_reader.requests, "get", mock_get)
    monkeypatch.setattr(
        webpage_reader.trafilatura,
        "extract",
        lambda *args, **kwargs: "Redirected content"
    )
    monkeypatch.setattr(
        webpage_reader.trafilatura,
        "extract_metadata",
        lambda *args, **kwargs: None
    )

    result = webpage_reader.extract_webpage("https://example.com")

    assert "Redirected content" in result
    assert calls == [
        "https://example.com",
        "https://example.org/page"
    ]


def test_extract_webpage_rejects_unsafe_redirect(monkeypatch):
    class MockResponse:
        status_code = 302
        headers = {"Location": "http://127.0.0.1"}
        text = ""

        def raise_for_status(self):
            pass

    monkeypatch.setattr(
        webpage_reader.requests,
        "get",
        lambda *args, **kwargs: MockResponse()
    )

    result = webpage_reader.extract_webpage("https://example.com")

    assert "Redirect destination is not allowed" in result

def test_extract_webpage_rejects_unsupported_content_type(monkeypatch):
    class MockResponse:
        status_code = 200
        headers = {"Content-Type": "application/pdf"}
        text = "PDF content"

        def raise_for_status(self):
            pass

    monkeypatch.setattr(
        webpage_reader.requests,
        "get",
        lambda *args, **kwargs: MockResponse()
    )

    result = webpage_reader.extract_webpage("https://example.com")

    assert "Unsupported content type" in result


@pytest.mark.parametrize("max_chars", [0, -1, 1.5, "100"])
def test_extract_webpage_rejects_invalid_max_chars(max_chars):
    result = webpage_reader.extract_webpage(
        "https://example.com",
        max_chars=max_chars
    )

    assert "max_chars must be a positive integer" in result


def test_extract_webpage_handles_redirect_without_location(monkeypatch):
    class MockResponse:
        status_code = 302
        headers = {}
        text = ""

        def raise_for_status(self):
            pass

    monkeypatch.setattr(
        webpage_reader.requests,
        "get",
        lambda *args, **kwargs: MockResponse()
    )

    result = webpage_reader.extract_webpage("https://example.com")

    assert "Redirect response has no Location header" in result
