import os
from dotenv import load_dotenv

from .schema import LinkedInPostSchema
from .instructions import linkedin_instructions

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')


model = LitellmModel(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key,
)

linkedin_agent = Agent(
    name="LinkedIn Post Writer Agent",
    model=model,
    instructions=linkedin_instructions,
    output_type=LinkedInPostSchema,
    
)
