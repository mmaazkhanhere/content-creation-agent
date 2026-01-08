import asyncio
import os
from dotenv import load_dotenv

from .schema import TwitterPostSchema
from .instructions import twitter_instructions
from logger import log

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
    model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=groq_api_key,
)



twitter_agent = Agent(
    name="Twitter Content Creator",
    model=model,
    instructions=twitter_instructions,
    output_type=TwitterPostSchema,
)

async def main():
    log("Generating Twitter content...", level="info")
    
    runner = await Runner.run(
    twitter_agent,
    f"""
         [09:17:30] ✅ PLAN 1: topic='Nvidia Rubin AI platform' 
         source_url='https://www.cnet.com/best-of-ces-2026/' thesis='The Nvidia Rubin AI 
         platform is a significant advancement in AI technology, offering six new Rubin 
         chips that lower the cost of AI tokens, which is crucial for compute-heavy models.' 
         why_now="The announcement of Nvidia's Rubin AI platform at CES 2026 highlights its 
         importance in the current AI landscape, making it a timely topic for discussion." 
         key_points=['Nvidia introduces the Rubin AI platform with six new chips.', 'These 
         chips aim to lower the cost of AI tokens.', 'This development is key for compute-heavy 
         AI models.', 'The platform was announced at CES 2026.', 'It signifies a major step 
         in making AI more accessible.'] target_audience='Tech enthusiasts and professionals 
         interested in AI advancements.' stance=<Stance.EDUCATIONAL: 'educational'> 
         writing_plan='Introduce the Nvidia Rubin AI platform and its significance, discuss 
         its features and implications, provide context on its announcement at CES 2026, 
         and conclude with its potential impact on the AI industry.' 
         confidence=<Confidence.HIGH: 'high'>
         [09:17:30] ✅ PLAN 2: topic='Lenovo Motorola Qira hybrid AI assistant' 
         source_url='https://www.cnet.com/best-of-ces-2026/' thesis='The Lenovo Motorola 
         Qira hybrid AI assistant represents a new frontier in AI interaction, offering a 
         cross-device on-device and cloud AI solution that competes with Apple Intelligence.
         ' why_now='As AI assistants become increasingly prevalent, the introduction of Qira 
         at CES 2026 makes it a relevant topic for discussion.' key_points=['Lenovo and
          Motorola introduce the Qira hybrid AI assistant.', 'It offers cross-device 
          functionality with both on-device and cloud AI.', 'Qira is positioned as a competitor 
          to Apple Intelligence.', 'The assistant was showcased at CES 2026.', 'It aims to 
          enhance user experience across devices.'] target_audience='Consumers and tech 
          professionals interested in AI assistants and smart devices.' 
          stance=<Stance.OPINIONATED: 'opinionated'> writing_plan='Introduce the Qira hybrid 
          AI assistant and its unique features, discuss its competitive positioning against 
          Apple Intelligence, analyze its potential market impact, and conclude with insights 
          on its future prospects.' confidence=<Confidence.HIGH: 'high'>
    """
)

    
    output = runner.final_output
    if output:
        log("Topic 1 Tweets:", level="success")
        for i, tweet in enumerate(output.topic_1_tweets, 1):
            log(f"Tweet {i}: {tweet}", level="success")
            
        log("\nTopic 2 Tweets:", level="success")
        for i, tweet in enumerate(output.topic_2_tweets, 1):
            log(f"Tweet {i}: {tweet}", level="success")
    else:
        log("Failed to generate tweets.", level="error")

if __name__ == "__main__":
    asyncio.run(main())