import os
from dotenv import load_dotenv

from .schema import LinkedInPostSchema
from .instructions import linkedin_instructions

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

BRAND_CONTEXT = {
    "role": "AI Engineer",
    "seniority": "Mid",
    "target_audience": ["Recruiters", "Hiring Managers", "AI Engineers"],
    "domains": ["LLMs", "AI Agents", "RAG", "Evaluations", "MLOps"],
    "tools": ["Python", "PyTorch", "LangGraph", "LangChain", "OpenAI Agent SDK", "Google SDK", "Docker", "FastAPI"],
    "voice": "practical, opinionated, calm",
    "goals": [
        "Build professional network",
        "Attract recruiter attention",
        "Demonstrate real-world AI expertise"
    ]
}



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
