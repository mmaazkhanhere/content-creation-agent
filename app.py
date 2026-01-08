import streamlit as st
import asyncio
from specialized_agents.personal_branding_agent import run_personal_branding_agent

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="BrandFlow",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- THEME-AWARE MINIMAL CSS (works in light + dark) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
}

/* Theme-aware tokens (Streamlit provides these in both light/dark) */
:root {
  --bg: var(--background-color);
  --panel: var(--secondary-background-color);
  --text: var(--text-color);
  --muted: rgba(128, 128, 128, 0.9);
  --border: rgba(128, 128, 128, 0.25);

  /* Brand accent (you can change this) */
  --accent: #2563eb;
}

/* Header */
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

/* Card */
.bf-card {
  border: 1px solid var(--border);
  background: var(--panel);
  border-radius: 14px;
  padding: 1.25rem 1.25rem;
  margin: 1rem 0 1.25rem 0;
}
.bf-topic {
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
  font-weight: 650;
  color: var(--text);
}
.bf-label {
  margin: 1rem 0 0.5rem 0;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}
.bf-content {
  border: 1px solid var(--border);
  background: color-mix(in srgb, var(--panel) 70%, var(--bg) 30%);
  border-radius: 10px;
  padding: 0.9rem 1rem;
  white-space: pre-wrap;
  line-height: 1.65;
  color: var(--text);
}

/* Tweet style */
.bf-tweet {
  border-left: 3px solid var(--accent);
  padding-left: 0.9rem;
  margin: 0.75rem 0;
  color: var(--text);
}
.bf-tweet small { color: var(--muted); }

/* Button: minimal, theme-friendly */
div.stButton > button {
  border-radius: 10px !important;
  padding: 0.6rem 1.25rem !important;
  font-weight: 650 !important;
  border: 1px solid var(--border) !important;
  background: var(--accent) !important;
  color: white !important;
}
div.stButton > button:hover {
  filter: brightness(0.95);
}

/* Expanders spacing */
div[data-testid="stExpander"] details {
  border-radius: 12px !important;
  border: 1px solid var(--border) !important;
}

/* Footer */
.bf-footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.85rem;
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="bf-header">
  <h1>BrandFlow</h1>
  <p>AI-powered content strategy for your personal brand.</p>
</div>
""", unsafe_allow_html=True)

# --- GENERATION TRIGGER ---
col_l, col_m, col_r = st.columns([1, 1, 1])
with col_m:
    if st.button("Generate Content", use_container_width=True):
        with st.spinner("Collaborating on your content..."):
            try:
                result = asyncio.run(run_personal_branding_agent())
                st.session_state.content = result
                st.success("Content ready.")
            except Exception as e:
                import traceback
                st.error(f"Error: {e}")
                st.expander("Details").code(traceback.format_exc())

st.write("")

# --- MAIN CONTENT ---
if "content" in st.session_state:
    data = st.session_state.content
    topics = data.topics if hasattr(data, "topics") else []

    for topic_data in topics:
        st.markdown(f"""
        <div class="bf-card">
          <div class="bf-content">{topic_data.topic}</div>
          <div class="bf-content">{topic_data.linkedin_post}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Twitter posts"):
            for j, tweet in enumerate(topic_data.twitter_tweets):
                st.markdown(f"""
                <div class="bf-tweet">
                  <strong>Tweet {j+1}</strong><br/>
                  {tweet}
                </div>
                """, unsafe_allow_html=True)

        with st.expander("Visual strategy"):
            prompt = topic_data.image_generation.image_1_prompt
            st.markdown(f"""
            <div class="bf-card" style="margin-top: 0.75rem;">
              <div class="bf-label" style="margin-top:0;">Prompt</div>
              <div class="bf-content">{prompt.prompt}</div>
              <div style="margin-top:0.65rem; color: var(--muted);">
                <small>Style: {prompt.style}</small>
              </div>
            </div>
            """, unsafe_allow_html=True)

else:
    st.info("Click **Generate Content** to begin.")

# --- FOOTER ---
st.markdown("""
<div class="bf-footer">
  BrandFlow • Created by mmaazkhan
</div>
""", unsafe_allow_html=True)
