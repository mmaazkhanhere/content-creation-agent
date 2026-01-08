import os

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
