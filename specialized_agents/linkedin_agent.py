import asyncio
import os
from pydantic.fields import Field
from pydantic.main import BaseModel
from dotenv import load_dotenv

from logger import log

from agents import Agent, Runner, trace
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

class LinkedInPostSchema(BaseModel):
    post: str = Field(description="LinkedIn post generated in markdown format")

model = LitellmModel(
    model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=groq_api_key,
)

instructions = """
You are an autonomous LinkedIn Post Writer Agent.
Using the provided content plan and brand context, write a single high-quality LinkedIn post.
The post must be clear, practical, and grounded in real information, reflecting an AI Engineer’s perspective.
Follow LinkedIn best practices: concise paragraphs, and a light call-to-action.
Do not search the web, invent facts, or output anything other than the final post text.
"""

linkedin_agent = Agent(
    name="LinkedIn Post Writer Agent",
    model=model,
    instructions=instructions,
    output_type=LinkedInPostSchema,
)

async def main():
    log("Writing Linkedin post...", level="info")
    
    runner = await Runner.run(
    linkedin_agent,
    f"""Plan: 
[18:38:08] ✅ SOURCE: https://9to5google.com/2026/01/06/moto-tag-2-announcement-ces-2026-android-find-hub/
[18:38:08] ✅ THESIS: The Moto Tag 2 represents a significant improvement in AI-powered tracking technology for Android devices, offering enhanced location accuracy, battery life, and durability.
[18:38:08] ✅ WHY_NOW: The recent launch of Moto Tag 2 at CES 2026 and its integration with Android 16 AI location services makes it a timely and relevant topic.
[18:38:08] ✅ KEY_POINTS: ['Motorola launched Moto Tag 2 at CES 2026 with enhanced tracking features.', 'Moto Tag 2 utilizes Bluetooth 6.0 Channel Sounding for improved location accuracy.', 'The device boasts a 500-day battery life and IP68 rating for durability.', 'Moto Tag 2 is the first UWB tracker to leverage Android 16 AI location services.', 'The launch of Moto Tag 2 signifies advancements in AI-powered Android Find Hub trackers.']
[18:38:08] ✅ AUDIENCE: Tech enthusiasts and Android users interested in tracking technology.
[18:38:08] ✅ STANCE: Stance.EDUCATIONAL
[18:38:08] ✅ CONFIDENCE: Confidence.HIGH
[18:38:08] ✅ PLAN_FOR_WRITE: Research the technology behind Moto Tag 2's tracking features, compare it with existing solutions, highlight user benefits, and discuss future implications for Android users."""
)

    
    linkedin_post = runner.final_output.post
    if linkedin_post:
        log(f"POST: {linkedin_post}", level="success")
    else:
        log("Failed to generate a post.", level="error")

if __name__ == "__main__":
    asyncio.run(main())