import os
import random
import difflib
from datetime import datetime

import requests
from dotenv import load_dotenv

from agents import Runner
from logger import log

from .meme_agent import meme_ideation_agent
from .planner_agent import search_agent

load_dotenv()

IMGFLIP_MEMES_URL = "https://api.imgflip.com/get_memes"
IMGFLIP_CAPTION_URL = "https://api.imgflip.com/caption_image"
DEFAULT_FALLBACK_TOPIC = "AI agents in production"


def _normalize_name(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum() or ch.isspace()).strip()


def _get_imgflip_templates() -> list[dict]:
    response = requests.get(IMGFLIP_MEMES_URL, timeout=15)
    response.raise_for_status()

    payload = response.json()
    if not payload.get("success"):
        raise RuntimeError("Imgflip template fetch failed")

    templates = payload.get("data", {}).get("memes", [])

    # Prefer two-box templates for consistent captioning via text0/text1.
    two_box_templates = [t for t in templates if int(t.get("box_count", 0)) == 2]
    if not two_box_templates:
        raise RuntimeError("No valid two-box Imgflip templates available")

    # Keep reasonably popular templates first.
    two_box_templates.sort(key=lambda t: int(t.get("captions", 0)), reverse=True)
    return two_box_templates[:60]


def _resolve_template(template_name: str, templates: list[dict]) -> dict:
    normalized_lookup = {_normalize_name(t["name"]): t for t in templates}
    normalized_target = _normalize_name(template_name)

    if normalized_target in normalized_lookup:
        return normalized_lookup[normalized_target]

    template_names = list(normalized_lookup.keys())
    close_matches = difflib.get_close_matches(normalized_target, template_names, n=1, cutoff=0.5)
    if close_matches:
        return normalized_lookup[close_matches[0]]

    return templates[0]

def _caption_imgflip(template_id: str, top_text: str, bottom_text: str) -> str:
    username = os.getenv("IMGFLIP_USERNAME")
    password = os.getenv("IMGFLIP_PASSWORD")

    if not username or not password:
        raise RuntimeError("Missing IMGFLIP_USERNAME or IMGFLIP_PASSWORD")

    response = requests.post(
        IMGFLIP_CAPTION_URL,
        data={
            "username": username,
            "password": password,
            "template_id": template_id,
            "text0": top_text,
            "text1": bottom_text,
        },
        timeout=20,
    )
    response.raise_for_status()

    payload = response.json()
    if not payload.get("success"):
        err = payload.get("error_message", "Unknown Imgflip caption error")
        raise RuntimeError(f"Imgflip caption failed: {err}")

    return payload["data"]["url"]


async def _discover_topic_context(user_topic: str | None) -> tuple[str, str | None]:
    today = datetime.now().strftime("%Y-%m-%d")
    topic_hint = user_topic.strip() if user_topic else ""

    prompt = (
        f"Date: {today}. Identify high-signal AI/LLM/RAG/agent topic details for Twitter meme ideation. "
        "Return concise research notes with topic candidates, supporting points, and source links."
    )
    if topic_hint:
        prompt += f" Prioritize this user topic: {topic_hint}."

    search_result = await Runner.run(search_agent, prompt)
    notes = str(search_result.final_output)

    if topic_hint:
        topic = topic_hint
    else:
        topic = "AI engineering trend from latest web signals"

    return topic, notes

async def run_twitter_meme_workflow(
    user_topic: str | None,
    source_mode: str,
    output_mode: str,
) -> dict:
    """
    Build 3 meme concepts and optional social posts.

    source_mode: "user_topic" | "web_search"
    output_mode: "meme_only" | "posts_only" | "meme_and_posts"
    """
    log("Starting Twitter meme workflow", level="info")

    if source_mode not in {"user_topic", "web_search"}:
        raise ValueError("Invalid source_mode")
    if output_mode not in {"meme_only", "posts_only", "meme_and_posts"}:
        raise ValueError("Invalid output_mode")

    topic = (user_topic or "").strip() or DEFAULT_FALLBACK_TOPIC
    research_notes = None

    if source_mode == "web_search":
        topic, research_notes = await _discover_topic_context(user_topic)

    templates = _get_imgflip_templates()
    template_options = "\n".join(f"- {t['name']} (id: {t['id']})" for t in templates)

    ideation_prompt = (
    f"Primary topic: {topic}\n"
    f"Output mode: {output_mode}\n"
    "Platform: Twitter/X only.\n"
    "Create 3 DISTINCT meme concepts that are genuinely funny, instantly understandable, and highly shareable on Twitter.\n"
    "The goal is not just to be clever — the meme should make technical people actually laugh because it feels painfully true.\n"
    "Humor style: sharp, dry, witty, self-aware, builder-minded, slightly ruthless about the problem, never rude for the sake of it.\n"
    "Make the joke feel like an insider observation from someone who understands AI, engineering, product, and internet culture.\n"
    "Ground the humor in real AI engineering pain points, contradictions, hype-vs-reality, workflow absurdities, and production headaches.\n"
    "Prioritize angles like: confident-but-wrong outputs, fake APIs, broken agent memory, context-window pain, fragile tool calling, eval fatigue, overengineered code, demo-vs-production gaps, and model churn.\n"
    "Avoid generic AI jokes, generic productivity jokes, safe corporate humor, stale meme phrasing, and anything that reads like LinkedIn cosplay.\n"
    "Avoid cringe, profanity, insults, politics, edgy humor, forced slang, and overexplaining the joke.\n"
    "The meme text must be SHORT, punchy, and readable in seconds while scrolling.\n"
    "Every meme should have a clear setup-payoff dynamic and a strong 'too real' effect.\n"
    "Choose template_name from the list below.\n"
    "Pick the template that makes the joke hit hardest, not the most obvious template.\n"
    "For Twitter post copy: write one very short caption per meme.\n"
    "The Twitter caption must feel native to X: concise, quotable, sharp, and complementary to the meme without repeating it word-for-word.\n"
    "Do not write threads. Do not write long context. Do not use hashtags unless absolutely necessary.\n"
    "The output should feel post-ready for Twitter and optimized for fast engagement.\n"
    "Each variation must use a DIFFERENT comedic angle, not just reword the same joke.\n"
    "Choose the funnier option over the safer option, as long as it stays tasteful and platform-safe.\n"
    f"Template options:\n{template_options}\n"
)
    if research_notes:
        ideation_prompt += f"\nWeb research notes:\n{research_notes}\n"

    ideation_result = await Runner.run(meme_ideation_agent, ideation_prompt)
    meme_plan = ideation_result.final_output

    versions = []
    generate_memes = output_mode in {"meme_only", "meme_and_posts"}

    # Randomize templates each run and avoid repeats across the 3 versions.
    if len(templates) >= len(meme_plan.memes):
        randomized_templates = random.sample(templates, k=len(meme_plan.memes))
    else:
        randomized_templates = [random.choice(templates) for _ in meme_plan.memes]

    for idx, concept in enumerate(meme_plan.memes):
        selected_template = randomized_templates[idx]
        meme_url = None

        if generate_memes:
            meme_url = _caption_imgflip(
                template_id=selected_template["id"],
                top_text=concept.top_text,
                bottom_text=concept.bottom_text,
            )

        versions.append(
            {
                "version": concept.version,
                "tone": concept.tone,
                "angle": concept.angle,
                "template_name": selected_template["name"],
                "template_id": selected_template["id"],
                "top_text": concept.top_text,
                "bottom_text": concept.bottom_text,
                "meme_caption": concept.meme_caption,
                "meme_url": meme_url,
                "twitter_post": concept.twitter_post,
                "linkedin_post": concept.linkedin_post,
            }
        )

    return {
        "topic": meme_plan.topic or topic,
        "source_mode": source_mode,
        "output_mode": output_mode,
        "research_notes": research_notes,
        "versions": versions,
    }





