import streamlit as st
import asyncio
from specialized_agents.personal_branding_agent import run_personal_branding_agent

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="BrandFlow AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

    :root {
        --primary: #6366f1;
        --secondary: #a855f7;
        --accent: #06b6d4;
        --bg-dark: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
    }

    /* Main App Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a, #020617);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
    }

    .hero-title {
        background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: -0.02em;
    }

    .hero-subtitle {
        color: var(--text-muted);
        text-align: center;
        font-size: 1.25rem;
        margin-bottom: 3rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Glassmorphism Card */
    .content-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        height: 100%;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    .content-card:hover {
        transform: translateY(-5px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 25px 30px -5px rgba(0, 0, 0, 0.2), 0 15px 15px -5px rgba(99, 102, 241, 0.1);
    }

    .topic-badge {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white;
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: inline-block;
        margin-bottom: 1.5rem;
    }

    .section-header {
        color: var(--accent);
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .linkedin-content {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.95rem;
        line-height: 1.6;
        color: #e2e8f0;
        white-space: pre-wrap;
    }

    .tweet-item {
        background: rgba(15, 23, 42, 0.3);
        border-left: 4px solid var(--primary);
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #cbd5e1;
    }

    .image-prompt-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 1px dashed rgba(168, 85, 247, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    .prompt-text {
        font-style: italic;
        color: #e2e8f0;
        margin-bottom: 10px;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 3rem !important;
        border-radius: 100px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.5) !important;
        display: block;
        margin: 0 auto !important;
    }

    div.stButton > button:hover {
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 15px 30px -5px rgba(168, 85, 247, 0.6) !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

    /* Hide Streamlit Header/Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Layout tweaks */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<h1 class="hero-title">BrandFlow</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Elevate your personal brand with AI-orchestrated content strategy. Generate platform-perfect posts for your professional niche in seconds.</p>', unsafe_allow_html=True)

# --- GENERATION TRIGGER ---
col_btn = st.columns([1, 1, 1])
with col_btn[1]:
    if st.button("✨ GENERATE CONTENT"):
        with st.spinner("🧠 Agents are collaborating on your strategy..."):
            try:
                # Running the async function using a more stable method for Streamlit
                # asyncio.run() creates a new loop every time, which is fine as long as 
                # background workers (like litellm's) are properly handled/disabled.
                result = asyncio.run(run_personal_branding_agent())
                st.session_state.content = result
                st.success("Analysis complete! Your content is ready.")
            except Exception as e:
                import traceback
                st.error(f"Execution Error: {e}")
                st.expander("Show full traceback").code(traceback.format_exc())

st.markdown("<br>", unsafe_allow_html=True)

# --- MAIN CONTENT DISPLAY ---
if "content" in st.session_state:
    data = st.session_state.content
    topics = data.topics if hasattr(data, 'topics') else []
    
    if len(topics) >= 2:
        # Side-by-side layout for large screens, stacks on small screens
        col1, col2 = st.columns([1, 1], gap="large")
        
        for i, (col, topic_data) in enumerate(zip([col1, col2], topics[:2])):
            with col:
                st.markdown(f"""
                <div class="content-card">
                    <span class="topic-badge">Topic {i+1}</span>
                    <h2 style="color: white; margin-bottom: 1rem; font-size: 1.8rem;">{topic_data.topic}</h2>
                """, unsafe_allow_html=True)
                
                # LinkedIn Section
                st.markdown('<div class="section-header">👔 LinkedIn Post</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="linkedin-content">{topic_data.linkedin_post}</div>', unsafe_allow_html=True)
                # Providing a code block for easy copying
                with st.expander("Copy raw LinkedIn post"):
                    st.code(topic_data.linkedin_post, language="markdown")
                
                # Twitter Section
                st.markdown('<div class="section-header">🐦 Twitter Posts</div>', unsafe_allow_html=True)
                for j, tweet in enumerate(topic_data.twitter_tweets):
                    st.markdown(f'<div class="tweet-item"><b>{j+1}.</b> {tweet}</div>', unsafe_allow_html=True)
                
                # Image Prompt Section
                st.markdown('<div class="section-header">🎨 Visual Strategy</div>', unsafe_allow_html=True)
                # Use image_1_prompt for the display as requested (one prompt per topic)
                prompt = topic_data.image_generation.image_1_prompt
                st.markdown(f"""
                <div class="image-prompt-card">
                    <p style="color: var(--secondary); font-weight: 700; font-size: 0.8rem; margin-bottom: 8px;">GENERATION PROMPT:</p>
                    <p class="prompt-text">"{prompt.prompt}"</p>
                    <div style="margin-top: 12px; display: flex; gap: 15px; font-size: 0.8rem;">
                        <span><b style="color: var(--accent);">Style:</b> {prompt.style}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Strategy engine returned insufficient data. Please re-run.")

else:
    # Empty State visual
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; opacity: 0.5;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">⚡</div>
        <h3 style="color: var(--text-muted);">Awaiting your command</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Click the button above to start the agentic workflow.</p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: var(--text-muted); font-size: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 2rem;">
    Powered by <b>Antigravity AI Agent Framework</b> • Created by <a href="https://linkedin.com/in/mmaazukhan" style="color: var(--primary); text-decoration: none;">mmaazkhan</a>
</div>
""", unsafe_allow_html=True)