import os
from dotenv import load_dotenv

from .schema import FinalContentOutput
from .instructions import final_output_instructions

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

model = LitellmModel(
    model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=groq_api_key,
)


final_output_agent = Agent(
    name="Final Output Agent",
    model=model,
    instructions=final_output_instructions,
    output_type=FinalContentOutput,
)