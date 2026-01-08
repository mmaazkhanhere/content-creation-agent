import os
import requests
from dotenv import load_dotenv

from agents import function_tool

from helper_functions import extract_content_text
from logger import log

load_dotenv()

@function_tool
def search_top_headlines(category: str):
    """
        Fetches a small, recent set of top news headlines in tech industry.

        Use this tool when you need to discover what topics are currently trending
        tech industry and category. Do NOT use this tool to fetch full article text,
        analyze content, or perform keyword-based searches.

        Input: category of supported type ["technology"]

        Output:
        - A structured result containing a bounded list of headlines with titles,
        URLs, and sources, or a structured error if the request fails.
    """
    log("Searching headlines", level="info")
    url = "https://gnews.io/api/v4/top-headlines"
    params = {
        "category": "technology",
        "lang": "en",
        "max": 4,
        "country": "us",
        "token": os.getenv("GNEWS_API_KEY")
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        headlines: list[dict[str, str]] = []

        for item in data.get("articles", []):
            if len(headlines) >= 2:
                break

            content = extract_content_text(item.get("url"))
            if not content:
                continue
            headlines.append({
                    "title": item.get("title"),
                    "url_link": item.get("url"),
                    "content": content
            })

        log("Headlines search successful", level="success")
        log(f"Headlines: {headlines}", level="info")
        return {
            "status": "success",
            "headlines": headlines,
            "error_code": None
        }
            
        
    except Exception as e:
        log(f"Headlines search failed: {e}", level="error")
        return {
            "status": "error",
            "headlines": [],
            "error_code": "API_ERROR",
        }


@function_tool
def search_news(query: str)->dict:
    """
        Searches recent news articles using Google News via SerpAPI.

        Use this tool when you want to discover recent news coverage
        related to a specific topic or query. Do NOT use this tool
        to fetch article content, summarize pages, or analyze text.

        Input:
        - query: A free-text search query describing the topic of interest.

        Output:
        - A structured result containing a bounded list of news article
        titles, URLs, and sources, or a structured error if the search fails.
    """
    log(f"Searching news for query: {query}", level="info")
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "tbm": "nws",         
        "num": 3,
        "hl": "en",
        "api_key": os.getenv("SERP_API_KEY")
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results: list[dict[str, str]] = []

        for item in data.get("news_results", []):
            if len(results) >= 2:
                break
            url_link = item.get("link")
            content = extract_content_text(url_link)
            if content:
                results.append({
                    "title": item.get("title"),
                    "url_link": url_link,
                    "content": content
                })
            
        log("News search successful", level="success")
        log(f"News search results: {results}", level="info")
        return {
            "status": "ok",
            "query": query,
            "results": results,
            "error_code": None,
        }
    except Exception as e:
        log(f"News search failed: {e}", level="error")
        return {
            "status": "error",
            "query": query,
            "results": [],
            "error_code": "API_ERROR",
        }