import os
from dotenv import load_dotenv

from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel

from .instructions import meme_ideation_instructions
from .schema import MemeIdeationOutput

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

model = LitellmModel(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key,
)

meme_ideation_agent = Agent(
    name="Twitter Meme Ideation Agent",
    model=model,
    instructions=meme_ideation_instructions,
    output_type=MemeIdeationOutput,
)
