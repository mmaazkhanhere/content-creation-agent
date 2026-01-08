import asyncio
from datetime import datetime

from .planner_agent import search_agent, planner_agent
from .linkedin_agent import linkedin_agent
from .twitter_agent import twitter_agent
from .image_generation_agent import image_generation_agent
from .final_output_agent import final_output_agent

from agents import Runner
from logger import log

async def run_personal_branding_agent():
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
    search_result = await Runner.run(search_agent, f"Search content for today's date: {datetime.now().strftime('%Y-%m-%d')}")
    log("Search Agent completed.", level="success")
    
    # 2. Planner Agent: Creates a content plan based on search results
    log("Calling Planner Agent...", level="info")
    planner_result = await Runner.run(planner_agent, f"Research Notes: {search_result.final_output}")
    log("Planner Agent completed.", level="success")
    
    # 3. Parallel Execution: LinkedIn, Twitter, and Image Generation Agents
    log("Calling LinkedIn, Twitter, and Image Generation Agents in parallel...", level="info")
    
    # Prepare the input for the content creation agents (the content plan)
    plan_input = str(planner_result.final_output)
    
    linkedin_task = Runner.run(linkedin_agent, f"Writing Plan: {plan_input}")
    twitter_task = Runner.run(twitter_agent, f"Writing Plan: {plan_input}")
    image_task = Runner.run(image_generation_agent, f"Writing Plan: {plan_input}")
    
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
    
    return final_result.final_output

if __name__ == "__main__":
    # Example usage for testing
    async def main():
        try:
            result = await run_personal_branding_agent()
            log("\n--- FINAL STRUCTURED OUTPUT ---")
            log(result)
        except Exception as e:
            log(f"Flow failed: {e}", level="error")

    asyncio.run(main())
