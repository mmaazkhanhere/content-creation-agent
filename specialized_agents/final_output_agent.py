import asyncio
import os
from dotenv import load_dotenv

from .schema import FinalContentOutput
from .instructions import final_output_instructions
from logger import log

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

async def main():
    log("Generating Final Output...", level="info")
    
    runner = await Runner.run(
    final_output_agent,
    f"""
         LinkedIn Posts: ✅ POST_1: ## Nvidia Rubin AI Platform: A Leap Forward in AI Technology
            The recent announcement of Nvidia's Rubin AI platform at CES 2026 marks a significant milestone in the advancement of AI technology. This platform introduces six new Rubin chips designed to lower the cost of AI tokens, a crucial development for compute-heavy AI models.
            The Rubin AI platform is poised to make AI more accessible by reducing the costs associated with AI computations. This is particularly important as AI models continue to grow in complexity and demand more computational resources.
            What makes this announcement timely is its potential to accelerate AI adoption across industries. By making AI computations more affordable, Nvidia's Rubin AI platform can enable more businesses and developers to build and deploy AI-powered applications.
            As AI engineers, we're excited to see how this development will shape the future of AI. I'd love to hear your thoughts on the implications of Nvidia's Rubin AI platform. How do you think it will impact the AI landscape?
            ## #AI #Nvidia #RubinAIPlatform #CES2026
            [10:18:54] ✅ POST_2: ## Lenovo Motorola Qira Hybrid AI Assistant: The Future of AI Interaction?
            The Lenovo Motorola Qira hybrid AI assistant, showcased at CES 2026, represents a new frontier in AI interaction. This innovative solution offers a cross-device, on-device, and cloud AI approach that competes directly with Apple Intelligence.
            What sets Qira apart is its ability to seamlessly integrate across devices, providing a cohesive user experience. This hybrid approach combines the benefits of on-device AI for privacy and security with the power of cloud AI for more complex tasks.
            As we continue to rely on AI assistants in our daily lives, solutions like Qira are poised to revolutionize how we interact with technology. While it's still early days, I'm excited to see how Qira will evolve and compete in the market.
            What are your thoughts on the Qira hybrid AI assistant? Do you think it has the potential to disrupt the AI assistant landscape?
            ## #AI #Lenovo #Motorola #Qira #CES2026
         X (Twitter Tweets): [10:19:50] ✅ Topic 1 Tweets:
[10:19:50] ✅ Tweet 1: Meet Nvidia's Rubin AI platform, a game-changer in AI tech! With six new chips, it's set to lower AI token costs, making compute-heavy models more accessible. #AIadvancements
[10:19:50] ✅ Tweet 2: Nvidia's Rubin AI platform is a significant leap forward! Announced at CES 2026, it brings six new chips that reduce AI token costs, crucial for AI models. Tech enthusiasts, take note!
[10:19:50] ✅ Tweet 3: What makes Nvidia's Rubin AI platform stand out? Its six new chips not only enhance performance but also lower AI token costs. A major step towards democratizing AI.
[10:19:50] ✅ Tweet 4: The future of AI is here with Nvidia's Rubin platform! By cutting AI token costs, it paves the way for more innovative AI applications. Kudos to Nvidia for pushing boundaries!
[10:19:50] ✅
Topic 2 Tweets:
[10:19:50] ✅ Tweet 1: Lenovo & Motorola unveil Qira, a hybrid AI assistant that's a direct competitor to Apple Intelligence! With cross-device on-device & cloud AI, it's set to revolutionize AI interaction.
[10:19:50] ✅ Tweet 2: Say hello to Qira, the latest innovation from Lenovo & Motorola! This hybrid AI assistant offers a seamless experience across devices, challenging Apple Intelligence. The AI game just changed!
[10:19:50] ✅ Tweet 3: What sets Qira apart from other AI assistants? Its unique blend of on-device & cloud AI for cross-device functionality. Lenovo & Motorola are redefining AI interaction with Qira.
[10:19:50] ✅ Tweet 4: The Qira hybrid AI assistant from Lenovo & Motorola is more than just a new player in the AI scene - it's a bold move towards enhancing user experience across devices. Watch out, Apple Intelligence! 
         Image Generation Prompt:  [10:20:13] ✅ Image Generation Prompt 1:
[10:20:13] ✅ Prompt 1: ('prompt', 'A futuristic data center with rows of servers powered by Nvidia Rubin AI platform chips, with a sleek and modern design')
[10:20:13] ✅ Prompt 2: ('style', 'neon-lit, cyberpunk')
[10:20:13] ✅ Prompt 3: ('notes', "Emphasize the cutting-edge technology and computational power of Nvidia's Rubin AI platform")
[10:20:13] ✅
Image Generation Prompt 2:
[10:20:13] ✅ Prompt 1: ('prompt', 'A person interacting with a Lenovo Motorola device that displays the Qira hybrid AI assistant interface, with a seamless blend of on-device and cloud AI features')
[10:20:13] ✅ Prompt 2: ('style', 'minimalist, product-focused')
[10:20:13] ✅ Prompt 3: ('notes', 'Highlight the user-friendly interface and cross-device functionality of Qira hybrid AI assistant')
    """
)

    
    output = runner.final_output
    if output:
        log(f"Final Output: {output}", level="success")
    else:
        log("Failed to generate structure output.", level="error")

if __name__ == "__main__":
    asyncio.run(main())