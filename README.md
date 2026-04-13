# BrandFlow: Multi-Agent AI Content Creation App

BrandFlow is a Streamlit application that orchestrates multiple AI agents to generate complete personal-brand content packs for AI engineering topics.  
For each run, it produces:
- 2 high-signal topics
- 2 LinkedIn posts (one per topic)
- Twitter/X tweet sets (one set per topic)
- Structured image-generation prompts aligned to each topic

The system is designed for practical, production-oriented AI content focused on LLMs, RAG, agents, and related engineering tradeoffs.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Run the App](#run-the-app)
- [How the Pipeline Works](#how-the-pipeline-works)
- [Output Contract](#output-contract)
- [Troubleshooting](#troubleshooting)
- [Security and Cost Notes](#security-and-cost-notes)
- [Contributing](#contributing)
- [License](#license)

## Overview
BrandFlow coordinates specialized LLM agents to turn current AI news and trends into ready-to-publish content artifacts.

The app:
1. Discovers topic signals from headlines and news search.
2. Plans exactly two topics with structured rationale.
3. Generates LinkedIn, Twitter/X, and image prompts in parallel.
4. Assembles everything into a strict Pydantic output schema.

## Key Features
- Multi-agent orchestration with typed outputs.
- Parallel content generation for speed (`asyncio.gather`).
- Topic discovery grounded in external sources.
- Fallback article extraction pipeline (Newspaper3k -> Readability -> visible HTML extraction).
- Streamlit UI for one-click content generation.
- Twitter-focused meme studio with Imgflip template selection and caption generation.
- Strong output constraints using Pydantic schemas.

## Architecture
```text
User Input (optional topic)
        |
        v
Search Agent
  - search_top_headlines (GNews)
  - search_news (SerpAPI)
  - article content extraction from URLs
        |
        v
Planner Agent
  - selects exactly 2 topics
  - returns structured TopTwoTopics schema
        |
        v
Parallel Generation
  - LinkedIn Post Writer Agent
  - Twitter Content Creator Agent
  - Image Prompt Creator Agent
        |
        v
Final Output Agent
  - merges all content
  - returns FinalContentOutput schema
```

## Project Structure
```text
.
|- app.py                               # Streamlit UI entrypoint
|- helper_functions.py                  # URL content extraction and fallbacks
|- logger.py                            # Console logger
|- specialized_agents/
|  |- instructions.py                   # Agent prompts/instructions
|  |- schema.py                         # Pydantic output schemas
|  |- tools.py                          # Function tools (GNews, SerpAPI)
|  |- planner_agent.py                  # Search + planning agents
|  |- linkedin_agent.py                 # LinkedIn generation agent
|  |- twitter_agent.py                  # Twitter/X generation agent
|  |- image_generation_agent.py         # Image prompt generation agent
|  |- final_output_agent.py             # Final structured aggregator agent
|  |- personal_branding_agent.py        # End-to-end orchestration pipeline
|  |- meme_agent.py                     # Groq meme ideation agent
|  |- meme_workflow.py                  # Imgflip meme rendering workflow
|- pyproject.toml                       # Project metadata/dependencies
|- uv.lock                              # Locked dependency graph
```

## Tech Stack
- Python 3.11+
- Streamlit
- `openai-agents` + LiteLLM integration
- Pydantic
- Requests
- BeautifulSoup4
- Newspaper3k
- Readability-LXML

Model providers used in current code:
- Groq (search/planner/image/final/meme agents)
- Google Gemini (LinkedIn/Twitter agents via LiteLLM routing)

## Prerequisites
- Python 3.11 (repo includes `.python-version` = `3.11`)
- API keys for:
  - Groq
  - Google (Gemini)
  - GNews
  - SerpAPI
  - Imgflip (username + password for meme rendering)

Optional but recommended:
- `uv` package manager for reproducible installs from `uv.lock`

## Environment Variables
Create a `.env` file in the repository root:

```env
GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_google_key
GNEWS_API_KEY=your_gnews_key
SERP_API_KEY=your_serpapi_key
IMGFLIP_USERNAME=your_imgflip_username
IMGFLIP_PASSWORD=your_imgflip_password
```

Variable usage:
- `GROQ_API_KEY`: Search, Planner, Image Prompt, Final Output, and Meme Ideation agents.
- `GOOGLE_API_KEY`: LinkedIn and Twitter generation agents.
- `GNEWS_API_KEY`: Top technology headlines tool.
- `SERP_API_KEY`: News search tool.
- `IMGFLIP_USERNAME` and `IMGFLIP_PASSWORD`: Imgflip meme rendering.

## Installation
### Option A: Using uv (recommended)
```bash
uv sync
```

### Option B: Using pip
```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Run the App
```bash
streamlit run app.py
```

Then open:
- `http://localhost:8501`

## How the Pipeline Works
1. User optionally enters a topic in the UI.
2. Orchestrator injects today's date and topic hint into the Search Agent.
3. Search tools fetch news links and extract article text from source pages.
4. Planner Agent selects exactly two topics and creates content plans.
5. LinkedIn, Twitter, and Image Prompt agents execute in parallel from the same plan.
6. Final Output Agent composes a strict `FinalContentOutput`.
7. Streamlit displays topic cards, tweets, and visual prompt strategy.
8. Meme Studio can generate 3 Twitter-focused meme versions from topic input or web-search-derived context.

## Output Contract
The personal-branding response follows `FinalContentOutput`:
- `topics` (exactly 2 items)
  - `topic`
  - `linkedin_post`
  - `twitter_tweets` (list of tweets)
  - `image_generation`
    - `image_1_prompt`
    - `image_2_prompt`
      - `prompt`
      - `style`
      - `notes`

The meme studio response returns 3 versions with:
- selected Imgflip template name/id
- top and bottom meme text
- generated meme URL (except posts-only mode)
- companion Twitter post
- coherent LinkedIn post

## Troubleshooting
- `Missing API key` or provider errors:
  - Confirm `.env` exists in project root and variable names match exactly.
- `No content generated`:
  - Some article URLs may block scraping; extraction has fallbacks but may still fail.
  - Retry with a specific topic to improve signal quality.
- `Imgflip errors`:
  - Verify `IMGFLIP_USERNAME` and `IMGFLIP_PASSWORD` are valid.
  - Ensure selected template IDs are available through Imgflip API.
- `ModuleNotFoundError`:
  - Reinstall dependencies with `uv sync` (preferred) or `pip install -e .`.
- `Streamlit app not loading`:
  - Ensure no other process is using port `8501`.

## Security and Cost Notes
- Never commit `.env` or API keys.
- LLM inference and external API calls can incur cost every run.
- Tune request frequency and retries before production usage at scale.

## Contributing
1. Fork the repo.
2. Create a feature branch.
3. Keep changes scoped and tested.
4. Open a PR with:
   - problem statement
   - design/approach
   - validation steps

Suggested improvements:
- Add automated tests for tool outputs and schema validation.
- Add retry/backoff and circuit-breaker strategy for external APIs.
- Add telemetry and latency/cost monitoring.

## License
This project is licensed under the Apache License 2.0.  
See `LICENSE` for details.
