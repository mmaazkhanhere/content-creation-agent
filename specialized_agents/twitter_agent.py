import os
from dotenv import load_dotenv

from .schema import TwitterPostSchema
from .instructions import twitter_instructions

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')


model = LitellmModel(
    model="gemini/gemini-2.5-flash-preview-09-2025",
    api_key=google_api_key,
)



twitter_agent = Agent(
    name="Twitter Content Creator",
    model=model,
    instructions=twitter_instructions,
    output_type=TwitterPostSchema,
)
