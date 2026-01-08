from pydantic import BaseModel, Field
from enum import Enum

#----- Planner Agent Schema -----#

class Stance(str, Enum):
    PRACTICAL = "practical"
    OPINIONATED = "opinionated"
    EDUCATIONAL = "educational"

class Confidence(str, Enum):
    HIGH = "high"
    LOW = "low"

class ContentPlan(BaseModel):
    topic: str = Field(description="The selected topic for the content.")
    source_url: str = Field(description="The URL of the source content.")
    thesis: str = Field(description="The detailed core opinion and takeaway from the content")
    why_now: str = Field(description="Justifying why writing about the topic matters now")
    key_points: list[str] = Field(description="List of key 5 key statements from the content")
    target_audience: str = Field(description="Who is the target audience for the content")
    stance: Stance = Field(description="What should be the stance when writing about the topic and content")
    writing_plan: str = Field(description="A concise plan (3-4 steps) on how to approach writing content for this topic to make it viral.")
    confidence: Confidence = Field(description="What is the confidence in proposing to write about this topic and content")

class TopTwoTopics(BaseModel):
    plan_1: ContentPlan = Field(description="The plan to write the first topic")
    plan_2: ContentPlan = Field(description="The plan to write the second topic")


#----- LinkedIn Post Generator Agent Schema --------#
class LinkedInPostSchema(BaseModel):
    post_1: str = Field(description="First LinkedIn post generated in markdown format")
    post_2: str = Field(description="Second LinkedIn post generated in markdown format")

#----- Twitter Post Generator Agent Schema --------#
class TwitterPostSchema(BaseModel):
    topic_1_tweets: list[str] = Field(description="A list of 4 distinct tweets for the first topic (PLAN 1)")
    topic_2_tweets: list[str] = Field(description="A list of 4 distinct tweets for the second topic (PLAN 2)")

#---- Image Generation Agent Schema --------#
class ImageGenerationPrompt(BaseModel):
    prompt: str = Field(description="The prompt describing the image to generate")
    style: str = Field(description="The visual style or aesthetic of the image to generate")
    notes: str = Field(description="Constraint or guidance for the image to generate")

class ImageGenerationSchema(BaseModel):
    image_1_prompt: ImageGenerationPrompt = Field(description="The prompt for the first image to generate")
    image_2_prompt: ImageGenerationPrompt = Field(description="The prompt for the second image to generate")
    