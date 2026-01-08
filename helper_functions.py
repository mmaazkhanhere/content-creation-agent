import time
import requests
from readability import Document as ReadabilityDocument
from bs4 import BeautifulSoup
from newspaper import Article
from newspaper import Config
from logger import log


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

MAX_HTML_BYTES = 750_000
MAX_ARTICLE_CHARS = 2500
REQUEST_TIMEOUT = 10

def clamp_text(text: str | None, limit: int = MAX_ARTICLE_CHARS) -> str | None:
    if text and len(text) > limit:
        return text[:limit]
    return text

def fetch_html(url: str, max_bytes: int = MAX_HTML_BYTES) -> tuple[str | None, str | None]:
    log(f"Fetching HTML from {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 403:
            return None, "FORBIDDEN"
        if response.status_code == 404:
            return None, "NOT_FOUND"
        response.raise_for_status()
        chunks = []
        total = 0
        for chunk in response.iter_content(chunk_size=64 * 1024):
            if not chunk:
                continue
            chunks.append(chunk)
            total += len(chunk)
            if total >= max_bytes:
                break

        raw = b"".join(chunks)

        # Best-effort decode (requests may not know encoding yet because we stopped early)
        encoding = response.encoding or "utf-8"
        html = raw.decode(encoding, errors="replace")
        return html, None
    except requests.Timeout:
        return None, "TIMEOUT"
    except requests.RequestException:
        return None, "NETWORK_ERROR"


def extract_article_text_newspaper(url: str) -> str | None:
    """Extract main article text from a given URL and is optimized for news articles and blog posts.
    It returns None if extraction fails or the extracted content is too short."""
    log(f"Extracting content with Newspaper3k from {url}")

    html, err = fetch_html(url)
    if err == "FORBIDDEN":
        log(f"Newspaper3k skipped (FORBIDDEN): {url}", level="warning")
        return None
    if not html:
        log(f"Newspaper3k skipped (fetch error: {err}): {url}", level="warning")
        return None
    try:
        config = Config()
        config.browser_user_agent = HEADERS["User-Agent"]
        config.request_timeout = REQUEST_TIMEOUT
        config.fetch_images = False
        
        article = Article(url, config=config)
        article.download(input_html=html)  
        article.parse()

        text = article.text.strip()
        if len(text) > 200:
            log("Newspaper3k extraction successful", level="success")
            return clamp_text(text)
        log("Newspaper3k extraction failed: Content too short", level="warning")
        return None
    except Exception as e:
        log(f"Error extracting content with Newspaper3k: {e}", level="error")
        return None

def extract_article_text_readability(html: str) -> str | None:
    """Extract content from HTML by removing unnecessary elements and returning main content
    It returns None if the extracted content is too short."""
    log(f"Extracting content with Readability")
    try:
        doc = ReadabilityDocument(html)
        summary = doc.summary()
        if not summary:
            log("Readability extraction failed: No summary found", level="warning")
            return None
        soup = BeautifulSoup(summary, 'html.parser')
        text = soup.get_text(separator="\n", strip=True)
        if len(text) > 200:
            log("Readability extraction successful", level="success")
            return text
        log("Readability extraction failed: Content too short", level="warning")
        return None
    except Exception as e:
        log(f"Error extracting content with Readability: {e}", level="error")
        return None

def extract_visible_text_html(html: str) -> str | None:
    """A fallback method that removes common non-content tags and returns clean visible text from HTML. 
    Returns None if content is too short or extraction fails."""
    log(f"Extracting content with Plain HTML")
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove noisy elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
            
        text = soup.get_text(separator="\n", strip=True)
        # Filter lines that look like main content (longer lines)
        lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 50]
        content = "\n".join(lines)
        
        if len(content) > 200:
            log("Plain HTML extraction successful", level="success")
            return content
        log("Plain HTML extraction failed: Content too short", level="warning")
        return None
    except Exception as e:
        log(f"Error extracting content with Plain HTML: {e}", level="error")
        return None

def extract_content_text(url: str) -> str | None:
    """
    Attempt multiple extraction methods sequentially until one succeeds.
    Gracefully handles blocked or inaccessible pages.
    """
    log(f"Starting extraction process for: {url}", level="info")

    text = extract_article_text_newspaper(url)
    if text:
        return text

    html, error_code = fetch_html(url)

    if error_code == "FORBIDDEN":
        log(f"Access forbidden for {url}. Skipping HTML-based extractors.", level="warning")
        return None

    if not html:
        log(f"Failed to fetch HTML for {url}. Error: {error_code}", level="error")
        return None

    for extractor in [
        extract_article_text_readability,
        extract_visible_text_html
    ]:
        try:
            text = extractor(html)
            if text:
                log(f"Successfully extracted {len(text)} chars using {extractor.__name__}", level="success")
                return clamp_text(text)
            time.sleep(0.5)
        except Exception as e:
            log(f"{extractor.__name__} failed: {e}", level="error")

    log(f"All extraction methods failed for url: {url}", level="error")
    return None



