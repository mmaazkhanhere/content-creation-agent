from dotenv import load_dotenv
import os

from agents import Agent, Runner, trace
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

model = LitellmModel(
    model_name="groq/groq-llama-3.2-70b-instruct",
    api_key=groq_api_key,
    max_tokens=1000,
    temperature=0.7,
    top_p=0.9,
    top_k=50,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop_sequences=["</s>"]
)

