import asyncio
from datetime import datetime

from .planner_agent import search_agent, planner_agent
from .linkedin_agent import linkedin_agent
from .twitter_agent import twitter_agent
from .image_generation_agent import image_generation_agent
from .final_output_agent import final_output_agent

from agents import Runner
from logger import log

BRAND_CONTEXT = {
  "brand_identity": {
    "title": "AI Engineer (LLM Apps, RAG & AI Agents)",
    "niche": ["LLM applications", "RAG systems", "AI agents", "LLM evaluations"],
    "value_proposition": "Builds and ships production-oriented AI systems, explains complex ideas simply, focuses on real-world constraints like cost, latency, and reliability",
    "differentiation": ["real deployments", "agent systems", "eval-driven design", "cost optimization"],
    "anti_brand": ["hype", "clickbait", "surface-level demos"]
  },
  "audience_and_goals": {
    "target_audiences": ["clients", "recruiters", "hiring_managers"],
    "target_roles": ["AI Engineer", "AI Agent Developer", "AI Fullstack Engineer"],
    "company_types": ["startups"],
    "geography_focus": "Europe (global audience)",
    "goals_90_days": {
      "interviews": "9+",
      "clients": "10+",
      "followers": "100+"
    },
    "monetization_timeline": "immediate",
    "brand_focus": "balanced (jobs + clients)"
  },
  "experience": {
    "years": {
      "ai_engineer": 2,
      "ml_engineer": 2
    },
    "focus_area": "building and scaling production-ready AI systems",
    "key_learning": "production reliability is harder than building demos"
  },
  "projects_and_proof": {
    "production_projects": [
      {
        "name": "CarBuddy Chatbot",
        "type": "LLM-powered customer support chatbot",
        "users": "UK car dealerships",
        "clients": ["DriveGreen", "Hudson Autos", "LM Motors"],
        "highlights": ["real customer usage", "production deployment"]
      },
      {
        "name": "AI Email Automation System",
        "type": "LLM-based customer outreach automation",
        "client": "Group1 Mercedes",
        "impact": "50k+ customers",
        "highlights": ["scalable automation", "business-facing AI"]
      }
    ],
    "hackathon_and_side_projects": [
      {
        "name": "Debating Agents",
        "description": "Multi-agent debate system that selects a winner based on reasoning quality",
        "tech": ["LangGraph", "AI agents"]
      },
      {
        "name": "SurgicalAI",
        "description": "Voice-based AI assistant for surgeons using RAG",
        "tech": ["RAG", "speech-to-text"],
        "data_sources": "Top surgical textbooks"
      },
      {
        "name": "AI Project Management Agent",
        "description": "Agent that assists with planning, tracking, and decision-making"
      },
      {
        "name": "Revisit",
        "description": "Multimodal therapy app to help users process memories",
        "modalities": ["text", "image", "audio", "video"]
      },
      {
        "name": "LearnPod",
        "description": "Video indexing platform using VLMs to make long videos searchable"
      },
      {
        "name": "AgentCuts",
        "description": "AI system that converts long videos into viral-ready short clips"
      }
    ],
    "credibility_signals": [
      "real production deployments",
      "hackathon-built AI systems",
      "latency and cost optimization experience",
      "AI/ML certifications"
    ],
    "assets": {
      "linkedin": "https://linkedin.com/in/mmaazukhan",
      "github": "https://github.com/mmaazkhanhere",
      "x": "https://x.com/mmaazkhanhere",
      "portfolio": "in_progress",
      "demo_videos": True
    }
  },
  "content_strategy": {
    "platforms": ["LinkedIn", "Twitter X"],
    "posting_frequency": {
      "linkedin": "1 post/week",
      "twitter_x": "multiple posts/day"
    },
    "content_pillars": [
      "production AI agent lessons",
      "RAG design mistakes and fixes",
      "LLM evals and guardrails in practice",
      "cost and latency optimization",
      "system design for LLM apps",
      "career guidance for junior/mid AI engineers"
    ],
    "tone": "friendly, fast, clear, practical",
    "reader_level": "mixed (junior to mid)"
  },
  "offers_and_ctas": {
    "services": ["RAG development", "LLM evals & guardrails", "AI agent workflows", "AI strategy"],
    "engagement_models": ["fixed_price", "monthly_retainer"],
    "call_to_actions": ["DM for projects or roles", "email/newsletter signup"]
  },
  "core_beliefs": {
    "agents": "Building AI agents is easy; building reliable production agents is hard",
    "engineering": "Strong AI systems still require real engineering judgment",
    "future": "AI will augment developers, not replace engineering fundamentals"
  }
}

async def run_personal_branding_agent(user_topic: str | None = None):
    """
    Main orchestration function for the personal branding content creation flow.
    
    1. Call Search Agent to find topics.
    2. Call Planner Agent to create a plan based on search results.
    3. Call LinkedIn, Twitter, and Image Generation Agents in parallel.
    4. Call Final Output Agent to assemble the results.
    
    Args:
        user_request (str): The initial user request or topic for content creation.
        
    Returns:
        FinalContentOutput: Structured response containing content for two topics.
    """
    log(f"Starting personal branding flow", level="info")
    
    # 1. Search Agent: Discovers current topics
    log("Calling Search Agent...", level="info")
    today = datetime.now().strftime('%Y-%m-%d')
    topic_hint = user_topic.strip() if user_topic else ""
    if topic_hint:
        search_prompt = (
            "Search content for today's date: "
            f"{today}. User topic provided: {topic_hint}. "
            "Prioritize this topic while staying within AI/LLM/RAG/agent scope."
        )
    else:
        search_prompt = (
            "Search content for today's date: "
            f"{today}. No user topic provided; generalize within AI/LLM/RAG/agent scope."
        )
    search_result = await Runner.run(search_agent, search_prompt)
    log("Search Agent completed.", level="success")
    
    # 2. Planner Agent: Creates a content plan based on search results
    log("Calling Planner Agent...", level="info")
    planner_result = await Runner.run(planner_agent, f"Research Notes: {search_result.final_output}")
    log("Planner Agent completed.", level="success")
    
    # 3. Parallel Execution: LinkedIn, Twitter, and Image Generation Agents
    log("Calling LinkedIn, Twitter, and Image Generation Agents in parallel...", level="info")
    
    # Prepare the input for the content creation agents (the content plan)
    plan_input = str(planner_result.final_output)
    
    linkedin_task = Runner.run(linkedin_agent, f"Writing Plan: {plan_input}", context=BRAND_CONTEXT)
    twitter_task = Runner.run(twitter_agent, f"Writing Plan: {plan_input}", context=BRAND_CONTEXT)
    image_task = Runner.run(image_generation_agent, f"Writing Plan: {plan_input}", context=BRAND_CONTEXT)
    
    # Run tasks in parallel using asyncio.gather
    linkedin_res, twitter_res, image_res = await asyncio.gather(
        linkedin_task, twitter_task, image_task
    )
    log("Parallel agents completed.", level="success")
    
    # 4. Final Output Agent: Assembles all content into a structured response
    log("Calling Final Output Agent...", level="info")
    combined_input = {
        "content_plan": planner_result.final_output,
        "linkedin_posts": linkedin_res.final_output,
        "twitter_tweets": twitter_res.final_output,
        "image_prompts": image_res.final_output
    }
    
    final_result = await Runner.run(final_output_agent, str(combined_input))
    log("Final Output Agent completed.", level="success")
    log(f"Final Output: {final_result.final_output}", level="info")
    
    return final_result.final_output

# if __name__ == "__main__":
#     # Example usage for testing
#     async def main():
#         try:
#             result = await run_personal_branding_agent()
#             log("\n--- FINAL STRUCTURED OUTPUT ---")
#             log(result)
#         except Exception as e:
#             log(f"Flow failed: {e}", level="error")

#     asyncio.run(main())
