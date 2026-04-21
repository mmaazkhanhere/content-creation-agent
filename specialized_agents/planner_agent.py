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
groq_search_model = os.getenv("GROQ_SEARCH_MODEL", "groq/llama-3.3-70b-versatile")
groq_planner_model = os.getenv(
    "GROQ_PLANNER_MODEL", "groq/meta-llama/llama-4-scout-17b-16e-instruct"
)

model_search = LitellmModel(
    model=groq_search_model,
    api_key=groq_api_key,
)

model_planner = LitellmModel(
    model=groq_planner_model,
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
