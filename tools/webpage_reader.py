import ipaddress
from urllib.parse import urljoin, urlsplit

import requests
import trafilatura
import truststore

# Use the Windows certificate store for corporate network TLS.
truststore.inject_into_ssl()


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
)

MAX_REDIRECTS = 5
REQUEST_TIMEOUT = 20


def validate_url(url: str) -> bool:
    """Validate HTTP/HTTPS URLs and reject obvious local addresses."""

    try:
        parsed = urlsplit(url)

        if parsed.scheme.lower() not in ("http", "https"):
            return False

        if not parsed.hostname or parsed.username or parsed.password:
            return False

        hostname = parsed.hostname.lower()

        if hostname == "localhost" or hostname.endswith(
            (".localhost", ".local")
        ):
            return False

        try:
            address = ipaddress.ip_address(hostname)

            if (
                address.is_private
                or address.is_loopback
                or address.is_link_local
                or address.is_multicast
                or address.is_reserved
                or address.is_unspecified
            ):
                return False

        except ValueError:
            pass

        return True

    except (ValueError, TypeError):
        return False


def extract_webpage(url: str, max_chars: int = 12000) -> str:
    """
    Fetch a webpage and extract readable text and available metadata.
    """

    if not url or not url.strip():
        return "Error: URL cannot be empty."

    if not validate_url(url):
        return "Error: Invalid or unsupported URL."

    if not isinstance(max_chars, int) or max_chars <= 0:
        return "Error: max_chars must be a positive integer."

    current_url = url.strip()

    try:
        headers = {"User-Agent": USER_AGENT}

        for redirect_count in range(MAX_REDIRECTS + 1):
            if not validate_url(current_url):
                return "Error: Redirect destination is not allowed."

            response = requests.get(
                current_url,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=False
            )

            if response.status_code in (301, 302, 303, 307, 308):
                location = response.headers.get("Location")

                if not location:
                    return "Error: Redirect response has no Location header."

                if redirect_count >= MAX_REDIRECTS:
                    return "Error: Maximum redirect limit exceeded."

                current_url = urljoin(current_url, location)
                continue

            response.raise_for_status()
            break

        content_type = response.headers.get("Content-Type", "").lower()

        if content_type and not any(
            allowed in content_type
            for allowed in ("text/html", "application/xhtml+xml")
        ):
            return f"Error: Unsupported content type: {content_type}"

        downloaded = trafilatura.extract(
            response.text,
            include_comments=False,
            include_tables=True,
            favor_recall=True
        )

        if not downloaded:
            return f"Could not extract readable content from: {current_url}"

        metadata = trafilatura.extract_metadata(response.text)

        metadata_output = ""

        if metadata:
            fields = {
                "Title": metadata.title,
                "Author": metadata.author,
                "Publication Date": metadata.date,
                "Website": metadata.sitename
            }

            metadata_output = "\n".join(
                f"{name}: {value}"
                for name, value in fields.items()
                if value
            )

        return (
            f"Source URL: {current_url}\n"
            f"HTTP Status: {response.status_code}\n"
            f"{metadata_output}\n"
            f"Extracted Content:\n{downloaded[:max_chars]}"
        )

    except requests.exceptions.RequestException as error:
        return f"Webpage request failed for {current_url}: {error}"

    except Exception as error:
        return f"Unexpected extraction error for {current_url}: {error}"
