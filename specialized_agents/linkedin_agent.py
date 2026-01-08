import asyncio
import os
from dotenv import load_dotenv

from .schema import LinkedInPostSchema
from .instructions import linkedin_instructions
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

linkedin_agent = Agent(
    name="LinkedIn Post Writer Agent",
    model=model,
    instructions=linkedin_instructions,
    output_type=LinkedInPostSchema,
)

async def main():
    log("Writing Linkedin post...", level="info")
    
    runner = await Runner.run(
    linkedin_agent,
    f"""
         PLAN 1: topic='OpenAI GPT-4.5 Turbo' source_url='https://techcrunch.com/2026/01/07/openai-gpt-4-5-turbo-rag-native-256k-context/' 
         thesis="OpenAI's GPT-4.5 Turbo offers a RAG-native architecture, 256k context, and highly competitive pricing, making it a significant advancement in AI technology." 
         why_now='The recent launch of GPT-4.5 Turbo by OpenAI is a timely development as it addresses current needs for more efficient, cost-effective, and powerful language models.' 
         key_points=['GPT-4.5 Turbo features a 256k context window.', 'It has a RAG-native architecture.', 'Pricing is under $0.10 per 1k token.',
        'This model is aimed at enhancing performance and reducing costs.', 'The launch signifies a major step forward in AI technology.'] target_audience='AI developers, 
        tech industry professionals, and businesses looking for advanced language model solutions.' stance=<Stance.EDUCATIONAL: 'educational'> writing_plan='Step 1: 
        Introduce the GPT-4.5 Turbo and its key features. Step 2: Discuss the implications of the RAG-native architecture and 256k context window. Step 3: 
        Analyze the cost benefits and potential market impact. Step 4: Explore potential applications and future developments.' confidence=<Confidence.HIGH: 'high'>
[19:18:17] ✅ PLAN 2: topic="LangChain's LongRAG" source_url='https://www.theverge.com/2026/01/07/langchain-longrag-million-token-rag-enterprise/' 
thesis="LangChain's LongRAG library enables the chunking of entire codebases into 1M-token contexts, facilitating advanced enterprise Q&A capabilities." 
why_now='The release of LongRAG by LangChain is timely as it addresses the growing need for more sophisticated and scalable solutions in enterprise Q&A.' 
key_points=['LongRAG allows for 1M-token context chunks.', 'It is designed for enterprise Q&A applications.', 'The library enables more comprehensive and 
context-aware querying.', 'This development is crucial for enterprises dealing with large codebases.', 'It enhances the capabilities of RAG systems in handling complex queries.'] 
target_audience='Enterprise developers, software engineers, and organizations looking to improve their Q&A systems.' 
stance=<Stance.PRACTICAL: 'practical'> writing_plan="Step 1: Introduce LangChain's LongRAG and its primary function. Step 2: Discuss the benefits of 1M-token context chunks for 
enterprise Q&A. Step 3: Explore the technical implementation and potential challenges. Step 4: Highlight case studies or potential applications." confidence=<Confidence.HIGH: 'high'>
    """
)

    
    linkedin_posts = runner.final_output
    if linkedin_posts:
        log(f"POST_1: {linkedin_posts.post_1}", level="success")
        log(f"POST_2: {linkedin_posts.post_2}", level="success")
    else:
        log("Failed to generate posts.", level="error")

if __name__ == "__main__":
    asyncio.run(main())