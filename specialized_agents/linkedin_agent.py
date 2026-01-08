import os
from dotenv import load_dotenv

from .schema import LinkedInPostSchema
from .instructions import linkedin_instructions

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')


model = LitellmModel(
    model="gemini/gemini-2.5-flash-preview-09-2025",
    api_key=google_api_key,
)

linkedin_agent = Agent(
    name="LinkedIn Post Writer Agent",
    model=model,
    instructions=linkedin_instructions,
    output_type=LinkedInPostSchema,
    
)
