import asyncio
import streamlit as st

from specialized_agents.personal_branding_agent import run_personal_branding_agent
from specialized_agents.meme_workflow import run_twitter_meme_workflow

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="BrandFlow",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
}

:root {
  --bg: var(--background-color);
  --panel: var(--secondary-background-color);
  --text: var(--text-color);
  --muted: rgba(128, 128, 128, 0.9);
  --border: rgba(128, 128, 128, 0.25);
  --accent: #2563eb;
}

.bf-header {
  text-align: center;
  margin: 2rem 0 1.25rem 0;
}
.bf-header h1 {
  margin: 0;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text);
}
.bf-header p {
  margin: 0.4rem 0 0 0;
  color: var(--muted);
  font-size: 1.05rem;
}

.bf-card {
  border: 1px solid var(--border);
  background: var(--panel);
  border-radius: 14px;
  padding: 1.1rem;
  margin: 0.85rem 0;
}

.bf-footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.85rem;
  margin-top: 2.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
}

div.stButton > button {
  border-radius: 10px !important;
  padding: 0.6rem 1.25rem !important;
  font-weight: 650 !important;
  border: 1px solid var(--border) !important;
  background: var(--accent) !important;
  color: white !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="bf-header">
  <h1>BrandFlow</h1>
  <p>AI-powered content strategy for personal brand and meme-led social content.</p>
</div>
""",
    unsafe_allow_html=True,
)

feature_mode = st.radio(
    "Feature",
    options=["Personal Branding Pack", "Twitter Meme Studio"],
    horizontal=True,
)

if feature_mode == "Personal Branding Pack":
    topic_input = st.text_input(
        "Topic (optional)",
        placeholder="e.g., RAG evaluation, AI agent reliability, vector DB tradeoffs",
        help="Leave blank for a general AI/LLM/RAG/agent topic search.",
    )

    col_l, col_m, col_r = st.columns([1, 1, 1])
    with col_m:
        if st.button("Generate Content", use_container_width=True):
            with st.spinner("Collaborating on your content..."):
                try:
                    cleaned_topic = topic_input.strip() if topic_input else ""
                    result = asyncio.run(
                        run_personal_branding_agent(user_topic=cleaned_topic or None)
                    )
                    st.session_state.content = result
                    st.success("Content ready.")
                except Exception as e:
                    import traceback

                    st.error(f"Error: {e}")
                    st.expander("Details").code(traceback.format_exc())

    if "content" in st.session_state:
        data = st.session_state.content
        topics = data.topics if hasattr(data, "topics") else []

        for topic_data in topics:
            with st.container(border=True):
                st.subheader(topic_data.topic)
                st.markdown(topic_data.linkedin_post)

            with st.expander("Twitter posts"):
                for j, tweet in enumerate(topic_data.twitter_tweets, start=1):
                    st.markdown(f"**Tweet {j}**")
                    st.write(tweet)

            with st.expander("Visual strategy"):
                prompt = topic_data.image_generation.image_1_prompt
                st.markdown(f"**Prompt:** {prompt.prompt}")
                st.caption(f"Style: {prompt.style}")
    else:
        st.info("Click **Generate Content** to begin.")

else:
    meme_topic = st.text_input(
        "Meme Topic (optional)",
        placeholder="e.g., prompt caching, agent evals, MCP reliability",
        help="Optional when source is web search. If provided, it will be prioritized.",
    )

    col1, col2 = st.columns(2)
    with col1:
        source_mode_label = st.selectbox(
            "Topic Source",
            options=["Use provided topic", "Use web search"],
            index=0,
        )
    with col2:
        output_mode_label = st.selectbox(
            "Output Mode",
            options=["Meme only", "LinkedIn + Twitter only", "Meme + LinkedIn + Twitter"],
            index=0,
        )

    source_mode = "user_topic" if source_mode_label == "Use provided topic" else "web_search"
    output_mode_map = {
        "Meme only": "meme_only",
        "LinkedIn + Twitter only": "posts_only",
        "Meme + LinkedIn + Twitter": "meme_and_posts",
    }
    output_mode = output_mode_map[output_mode_label]

    col_l, col_m, col_r = st.columns([1, 1, 1])
    with col_m:
        if st.button("Generate Meme Content", use_container_width=True):
            with st.spinner("Generating 3 Twitter-focused meme versions..."):
                try:
                    result = asyncio.run(
                        run_twitter_meme_workflow(
                            user_topic=(meme_topic.strip() or None),
                            source_mode=source_mode,
                            output_mode=output_mode,
                        )
                    )
                    st.session_state.meme_content = result
                    st.success("Meme studio output ready.")
                except Exception as e:
                    import traceback

                    st.error(f"Error: {e}")
                    st.expander("Details").code(traceback.format_exc())

    if "meme_content" in st.session_state:
        meme_data = st.session_state.meme_content
        st.subheader(f"Topic: {meme_data['topic']}")

        if meme_data.get("research_notes"):
            with st.expander("Web research notes used"):
                st.code(meme_data["research_notes"])

        for item in meme_data.get("versions", []):
            with st.container(border=True):
                st.markdown(f"### Version {item['version']}")
                st.caption(f"Tone: {item['tone']} | Template: {item['template_name']} (ID: {item['template_id']})")
                st.write(f"**Angle:** {item['angle']}")

                if output_mode in {"meme_only", "meme_and_posts"} and item.get("meme_url"):
                    st.image(item["meme_url"], use_container_width=True)
                    st.write(f"**Top text:** {item['top_text']}")
                    st.write(f"**Bottom text:** {item['bottom_text']}")
                    st.write(f"**Caption:** {item['meme_caption']}")

                if output_mode in {"meme_only", "meme_and_posts", "posts_only"}:
                    st.write("**Twitter Post**")
                    st.write(item["twitter_post"])

                if output_mode in {"posts_only", "meme_and_posts"}:
                    st.write("**LinkedIn Post**")
                    st.write(item["linkedin_post"])
    else:
        st.info("Click **Generate Meme Content** to create 3 versions.")

st.markdown(
    """
<div class="bf-footer">
  BrandFlow &bull; Created by mmaazkhan
</div>
""",
    unsafe_allow_html=True,
)
