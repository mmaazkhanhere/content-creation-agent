import asyncio
import os
from dotenv import load_dotenv

from .schema import ImageGenerationSchema
from .instructions import image_generation_instructions
from logger import log

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

model = LitellmModel(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key,
)


image_generation_agent = Agent(
    name="Image Generation Prompt Creator Agent",
    model=model,
    instructions=image_generation_instructions,
    output_type=ImageGenerationSchema,
)
