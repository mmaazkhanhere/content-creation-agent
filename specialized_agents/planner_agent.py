import os
import asyncio

from datetime import datetime
from dotenv import load_dotenv

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel


from .schema import TopTwoTopics
from .tools import search_top_headlines, search_news
from .instructions import search_instructions, planner_instructions
from logger import log

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

model_search = LitellmModel(
    model="groq/moonshotai/kimi-k2-instruct-0905",
    api_key=groq_api_key,
)

model_planner = LitellmModel(
    model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=groq_api_key,
)



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
    output_type=TopTwoTopics
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

    
    plans = planner_result.final_output
    if plans:
        log(f"PLAN 1: {plans.plan_1}", level="success")
        log(f"PLAN 2: {plans.plan_2}", level="success")
    else:
        log("Planner failed to generate a plan.", level="error")

if __name__ == "__main__":
    asyncio.run(main())