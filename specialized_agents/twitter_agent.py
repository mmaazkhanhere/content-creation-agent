import os
from dotenv import load_dotenv

from .schema import TwitterPostSchema
from .instructions import twitter_instructions

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')


model = LitellmModel(
    model="groq/qwen/qwen3-32b",
    api_key=groq_api_key,
)



twitter_agent = Agent(
    name="Twitter Content Creator",
    model=model,
    instructions=twitter_instructions,
    output_type=TwitterPostSchema,
)
