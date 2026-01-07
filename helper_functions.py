import requests
from readability import Document as ReadabilityDocument
from bs4 import BeautifulSoup
from newspaper import Article
from logger import log

def extract_article_text_newspaper(url: str) -> str | None:
    """Extract main article text from a given URL and is optimized for news articles and blog posts.
    It returns None if extraction fails or the extracted content is too short."""
    log(f"Extracting content with Newspaper3k from {url}")
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text.strip()
        if len(text) > 200:
            log("Newspaper3k extraction successful", level="success")
            return text
        log("Newspaper3k extraction failed: Content too short", level="warning")
        return None
    except Exception as e:
        log(f"Error extracting content with Newspaper3k: {e}", level="error")
        return None

def extract_article_text_readability(url: str) -> str | None:
    """Extract content from url by removing unnecessary elements and returning main content
    It returns None if extraction fails or the extracted content is too short."""
    log(f"Extracting content with Readability from {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        html = response.text
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

def extract_visible_text_html(url: str) -> str | None:
    """A fallback method that removes common non-content tags and returns clean visible text. Returns
    None if content is too short or extraction fails."""
    log(f"Extracting content with Plain HTML from {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        html = response.text
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
    """Attempt multiple extraction methods sequentially until one succeeds."""
    extractors = [
        extract_article_text_newspaper,
        extract_article_text_readability,
        extract_visible_text_html
    ]
    
    log(f"Starting extraction process for: {url}", level="highlight")
    
    for extractor in extractors:
        try:
            text = extractor(url)
            if text:
                return text
        except Exception as e:
            log(f"Extractor {extractor.__name__} raised an exception: {e}", level="error")
            continue
            
    log(f"All extraction methods failed for url: {url}", level="error")
    return None


