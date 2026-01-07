import os
import asyncio
import requests
from datetime import datetime
from dotenv import load_dotenv
from enum import Enum

from pydantic import BaseModel, Field
from agents import Agent, Runner, trace, function_tool
from agents.extensions.models.litellm_model import LitellmModel

from helper_functions import extract_content_text
from logger import log

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

@function_tool
def search_top_headlines(category: str):
    """
        Fetches a small, recent set of top news headlines in tech industry and doesn't 
        require any input parameter to be passed.

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
        "max": 6,
        "country": "us",
        "token": os.getenv("GNEWS_API_KEY")
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        headlines: list[dict[str, str]] = []

        for item in data.get("articles", []):
            content = extract_content_text(item.get("url"))
            if content:
                headlines.append({
                    "title": item.get("title"),
                    "url_link": item.get("url"),
                    "content": content
                })
            if len(headlines) >= 4:
                break
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

        for item in data.get("news_results", [])[:3]:
            url_link = item.get("link")
            content = extract_content_text(url_link)
            if content:
                results.append({
                    "title": item.get("title"),
                    "url_link": url_link,
                    "content": content
                })
            if len(results) >= 2:
                break
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

class Stance(str, Enum):
    PRACTICAL = "practical"
    OPINIONATED = "opinionated"
    EDUCATIONAL = "educational"

class Confidence(str, Enum):
    HIGH = "high"
    LOW = "low"

class ContentPlan(BaseModel):
    topic: str = Field(description="The selected topic for the content.")
    source_url: str = Field(description="The URL of the source content.")
    thesis: str = Field(description="The detailed core opinion and takeaway from the content")
    why_now: str = Field(description="Justifying why writing about the topic matters now")
    key_points: list[str] = Field(description="List of key 5 key statements from the content")
    target_audience: str = Field(description="Who is the target audience for the content")
    stance: Stance = Field(description="What should be the stance when writing about the topic and content")
    writing_plan: str = Field(description="A concise plan (3-4 steps) on how to approach writing content for this topic to make it viral.")
    confidence: Confidence = Field(description="What is the confidence in proposing to write about this topic and content")

model_search = LitellmModel(
    model="groq/llama-3.1-8b-instant",
    api_key=groq_api_key,
)

model_planner = LitellmModel(
    model="groq/openai/gpt-oss-120b",
    api_key=groq_api_key,
)

search_instructions = """
You are an autonomous Search Agent that proactively discovers current topics worth writing about.
Independently choose relevant queries and categories related to AI, RAG, LLM, engineering, startups, and AI Agents only.
Use `search_top_headlines` and `search_news` as needed; tool use is expected.
Return concise bullet-point findings referencing real article titles, sources and content only.
If no strong signals are found, clearly state this and stop.
"""

planner_instructions = """
You are an autonomous Planning Agent. Choose ONE topic strictly from the provided RESEARCH NOTES.
You must select a source_url that appears verbatim in the RESEARCH NOTES, and every key_statment must be supported by that source.
If the notes do not contain a strong AI/LLM/RAG/Agents topic with a credible source URL, return no None for output fields.
Return valid JSON matching the schema only; do not add fields and do not write the final content.
Do not guess, generalize, or introduce facts not present in the notes.
"""

search_agent = Agent(
    name="Search Agent",
    model=model_search,
    instructions=search_instructions,
    tools=[search_top_headlines, search_news]
)



planner_agent = Agent(
    name="Planner Agent",
    model=model_planner,
    instructions=planner_instructions,
    output_type=ContentPlan
)

async def main():
    log("Starting Search Agent...", level="info")
    search_result = await Runner.run(search_agent, f"Current date: {datetime.now().strftime('%Y-%m-%d')}")
    search_text = search_result.final_output
    
    if not search_text:
        log("No search results found.", level="error")
        return

    log("Search completed. Starting Planner Agent...", level="info")
    planner_result = await Runner.run(
    planner_agent,
    f"Current date: {datetime.now():%Y-%m-%d}\n\nRESEARCH NOTES:\n{search_text}"
)

    
    plan = planner_result.final_output
    if plan:
        log(f"TOPIC: {plan.topic}", level="success")
        log(f"SOURCE: {plan.source_url}", level="success")
        log(f"THESIS: {plan.thesis}", level="success")
        log(f"WHY_NOW: {plan.why_now}", level="success")
        log(f"KEY_POINTS: {plan.key_points}", level="success")
        log(f"AUDIENCE: {plan.target_audience}", level="success")
        log(f"STANCE: {plan.stance}", level="success")
        log(f"CONFIDENCE: {plan.confidence}", level="success")

        log(f"PLAN: {plan.writing_plan}", level="success")
    else:
        log("Planner failed to generate a plan.", level="error")

if __name__ == "__main__":
    asyncio.run(main())