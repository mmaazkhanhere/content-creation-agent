from dotenv import load_dotenv
import os
import requests

from agents import Agent, Runner, trace, function_tool
from agents.extensions.models.litellm_model import LitellmModel

from helper_functions import extract_content_text

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

@function_tool
def search_top_headlines(category: str):
    """A function to search for top headlines related to tech field."""
    url = "https://gnews.io/api/v4/top-headlines"

    params = {
        "category": category,
        "lang": "en",
        "max": 5,
        "token": os.getenv("GNEWS_API_KEY")
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        return response.json()
    except Exception as e:
        return {"status": "error", "error": f"Error fetching headlines related to: {category}"}

@function_tool
def search_web(query: str)->list[dict]:
    """A function that uses SerAPI to search web for given query and return list of title and link."""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "tbm": "nws",         
        "num": 5,
        "hl": "en",
        "api_key": os.getenv("SERP_API_KEY")
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        articles = []
        for item in data.get("news_results", []):
            articles.append({
                "title": item.get("title"),
                "url_link": item.get("link")
            })

        for article in articles:
            article["content"] = extract_content_text(article["url_link"])
        return articles
    except Exception as e:
        return {"status": "error", "error": f"Error fetching web search results related to query: `{query}`"}
    
    

# model = LitellmModel(
#     model="groq/llama-3.1-8b-instant",
#     api_key=groq_api_key,
# )

# instructions = """
# You are a content planner for a social media influencer. Your task is to generate a list of 5 relevant AI topics for building personal brand.
# """

# agent = Agent(
#     name="Planner Agent",
#     model=model,
#     instructions=instructions,
#     tools=[WebSearchTool()]
# )

# async def main():
#     plan = await Runner.run(agent, "Generate a list of 5 relevant AI topics for building personal brand.")
#     print(plan)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())