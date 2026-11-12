
import requests
import trafilatura
import truststore

# Use the Windows certificate store for corporate network TLS.
truststore.inject_into_ssl()

def extract_webpage(url: str, max_chars: int = 12000) -> str:
    """
    Fetch a webpage and extract its readable text.
    """

    if not url or not url.strip():
        return "Error: URL cannot be empty."

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        downloaded = trafilatura.extract(
            response.text,
            include_comments=False,
            include_tables=True,
            favor_recall=True
        )

        if not downloaded:
            return f"Could not extract readable content from: {url}"

        content = downloaded[:max_chars]

        return (
            f"Source URL: {url}\n"
            f"HTTP Status: {response.status_code}\n"
            f"Extracted Content:\n{content}"
        )

    except requests.exceptions.RequestException as error:
        return f"Webpage request failed for {url}: {error}"

    except Exception as error:
        return f"Unexpected extraction error for {url}: {error}"
